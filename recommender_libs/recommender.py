#!coding=utf-8
import json
import sys
from collections import Counter

from _vionel_helper import *
from _db_helper import MongoManager


class SimilarityRecommender(object):

    def __init__(self, db_name='VionelMovies', collection_name='BoxerMovies', hostname='172.17.42.1', port=27017):

        self.feature_weight_dict = {
            'imdbDirector': 0.7,
            'imdbGenre': 0.5,
            'imdbKeyword': 0.6,
            'wikiKeyword': 1.3,
            'vionelTheme': 1.3,
            'vionelScene': 0.35,
            'locationCountry': 0.3,
            'locationCity': 0.5,
            'imdbMainactor': 0.9,
            'RGB': 0.25,
            'brightness': 0.25
        }
        self.mongo_manager = MongoManager(db_name, collection_name, hostname, port)


    def __get_imdbid_feature_dict(self, feature_name):
        result_dict = {}
        all_movies_feature_dict_list = self.mongo_manager.exec_query({}, {"imdbId": 1, feature_name: 1, "_id": 0})

        for movie in all_movies_feature_dict_list:
            imdbid = movie["imdbId"]
            try:
                feature = movie[feature_name]
                result_dict[imdbid] = feature
            except KeyError:
                continue

        return result_dict



    def __get_imdbid_similarity_dict(self, movieid_list, recommended_by):

        movieid_with_featureid_dict = {}
        input_featureid_with_number_dict = {}

        movieid_with_featureid_dict = self.__get_imdbid_feature_dict(recommended_by)

        result_dict = {}
        if recommended_by == "imdbDirector" or recommended_by == "imdbGenre" or recommended_by == "locationCountry" or recommended_by == "locationCity" or recommended_by == "vionelScene" or recommended_by == "imdbMainactor" or recommended_by == "RGB" or recommended_by == "brightness":

            input_featureid_with_number_dict = intersection_of_values_for_certain_keys(movieid_list, movieid_with_featureid_dict)
            all_featureid_list = input_featureid_with_number_dict.keys()

            for k, v in movieid_with_featureid_dict.items():
                intersection_list = list(set(v).intersection(set(all_featureid_list)))
                if not intersection_list:
                    result_dict[k] = 0
                    continue
                compared_movie_feature_num_dict = intersection_of_values_for_certain_keys([k], movieid_with_featureid_dict)
                cosine_score = calculate_cosine(input_featureid_with_number_dict, compared_movie_feature_num_dict)
                result_dict[k] = cosine_score

            return result_dict

        else:
            input_movie_features = []
            input_movie_features = union_of_values_for_spec_keys(movieid_list, movieid_with_featureid_dict)

            coefficient = 0.1
            for k, v in movieid_with_featureid_dict.items():
                intersection_num = len(list(set(v).intersection(set(input_movie_features))))
                score = intersection_num * coefficient
                if score > 1:
                    score = 1
                result_dict[k] = score

            return result_dict



    def __language_filter(self, input_movieid_list, combined_movieid_sim_counter):

        imdbid_language_dict = self.__get_imdbid_feature_dict("language")

        languages_in_liked_list = []
        for item in input_movieid_list:
            try:
                languages_in_liked_list += imdbid_language_dict[item]
            except KeyError:
                continue

        languages_in_liked_list = list(set(languages_in_liked_list))

        delete_list = []
        for imdbid in combined_movieid_sim_counter:
            language_list = imdbid_language_dict[imdbid]
            if not language_list:
                continue
            intersection_list = list(set(languages_in_liked_list).intersection(set(language_list)))
            if not intersection_list: # 如果为空,则排除此电影
                delete_list.append(imdbid)

        for x in delete_list:
            del combined_movieid_sim_counter[x]

        return combined_movieid_sim_counter


    def __multiply_coefficient(self, movieid_score_counter, coefficient):
        result_count = Counter()
        for k, v in movieid_score_counter.items():
            result_count[k] = v * coefficient
        return result_count


    def features_contribute_most(self, recommended_movies_dict):
        """Get the features that contribute most for each recommended movie."""
        movieid_featurescore_dict = {}
        for movieid in recommended_movies_dict:
            feature_score_dict = {}
            for feature in self.feature_weight_dict:
                variable_name = feature.lower()
                exec "feature_score_dict['%s'] = self.%s_movieid_sim_counter['%s']" % (feature, variable_name, movieid)
            movieid_featurescore_dict[movieid] = feature_score_dict
        return movieid_featurescore_dict


    def recommend_for_each_feature(self, input_movieid_list, num_of_recommended_movies):
        """Generate variables dynamicly

            Generate 'self.imdbdirectors_movieid_sim_counter' this kind
            of variables.
            We will generate for each feature which will be used in the
            following steps.

        """

        for feature in self.feature_weight_dict:
            feature_movieid_sim_dict = self.__get_imdbid_similarity_dict(input_movieid_list, feature)
            feature_movieid_sim_counter = Counter(feature_movieid_sim_dict)
            feature_movieid_sim_counter = self.__multiply_coefficient(feature_movieid_sim_counter, self.feature_weight_dict[feature])

            for movieid in input_movieid_list:
                del feature_movieid_sim_counter[movieid]

            variable_name = feature.lower()
            exec "self.%s_movieid_sim_counter = feature_movieid_sim_counter" % variable_name


    def recommend(self, input_movieid_list, num_of_recommended_movies):
        """Return recommended movies and the features that contribute most in this recommendation.
            Format of the return(if num_of_recommended_movies is 2):
            {
                "movie": {
                            "tt0340855": 0.6837561795878957,
                            "tt1124035": 0.9627459173643833,
                         },
                "reason": {
                            "tt0340855": {
                                  "imdbDirector": 0,
                                  "brightness": 0.025,
                                  "locationCountry": 0.21213203435596423,
                                  "vionelTheme": 0.13,
                                  "RGB": 0.0625,
                                  "locationCity": 0.20412414523193148,
                                  "wikiKeyword": 0,
                                  "imdbGenre": 0.05,
                                  "vionelScene": 0,
                                  "imdbMainactor": 0,
                                  "imdbKeyword": 0
                                },
                            "tt1124035": {
                                  "imdbDirector": 0,
                                  "brightness": 0,
                                  "locationCountry": 0.21213203435596423,
                                  "vionelTheme": 0,
                                  "RGB": 0.0625,
                                  "locationCity": 0.15811388300841897,
                                  "wikiKeyword": 0.13,
                                  "imdbGenre": 0.05,
                                  "vionelScene": 0.35,
                                  "imdbMainactor": 0,
                                  "imdbKeyword": 0
                        }
            }

        """

        self.recommend_for_each_feature(input_movieid_list, num_of_recommended_movies)

        combined_movieid_sim_counter = Counter()
        for feature in self.feature_weight_dict:
            exec "combined_movieid_sim_counter += self.%s_movieid_sim_counter" % feature.lower()

        # filter
        combined_movieid_sim_counter = self.__language_filter(input_movieid_list, combined_movieid_sim_counter)
        final_recommended_movies_dict = dict(combined_movieid_sim_counter.most_common(num_of_recommended_movies))

        movieid_featurewithscore_dict = self.features_contribute_most(final_recommended_movies_dict)

        # print reason_tuple_list
        result_dict = dict()
        result_dict["movie"] = final_recommended_movies_dict
        result_dict["reason"] = movieid_featurewithscore_dict

        return result_dict


###########################################################################
###########################################################################

if __name__ == '__main__':
    movieid = 'tt0308055'
    sr = SimilarityRecommender('VionelMovies', 'TestCollection')
    result = sr.recommend([movieid], 10)
    result_json = json.dumps(result)
    print result_json




