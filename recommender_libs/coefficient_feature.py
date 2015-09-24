#!coding=utf-8
import json
import math
from recommender_helper import RecommenderHelper
from recommender_db import RecommenderDB
from recommender import recommend
from collections import Counter


class CoefficientFeature:

    recommender_db = RecommenderDB()

    def __init__(self):
        self.imdbid_genre_dict = self.recommender_db.get_imdbid_feature_dict("genre")
        self.imdbid_actor_dict = self.recommender_db.get_imdbid_feature_dict("actor")
        self.imdbid_imdbkeyword_dict = self.recommender_db.get_imdbid_feature_dict("imdbkeyword")
        self.imdbid_wikikeyword_dict = self.recommender_db.get_imdbid_feature_dict("wikikeyword")
        self.imdbid_vioneltheme_dict = self.recommender_db.get_imdbid_feature_dict("vioneltheme")
        self.imdbid_vionelscene_dict = self.recommender_db.get_imdbid_feature_dict("vionelscene")
        self.imdbid_locationcity_dict = self.recommender_db.get_imdbid_feature_dict("locationcity")
        self.imdbid_locationcountry_dict = self.recommender_db.get_imdbid_feature_dict("locationcountry")





    def __getCosSim(self, indict1, indict2):
        
        indict1_keys = indict1.keys()
        indict2_keys = indict2.keys()
        all_keys = list(set(indict1_keys + indict2_keys))
        indict1_keys_vector = [0] * len(all_keys)
        indict2_keys_vector = [0] * len(all_keys)
        
        for index, key in enumerate(all_keys):
            if key in indict1:
                indict1_keys_vector[index] = indict1[key]
            if key in indict2:
                indict2_keys_vector[index] = indict2[key]


        num1 = sum(map(lambda x: indict1_keys_vector[x] * indict2_keys_vector[x], range(0, len(all_keys))))
        tmp1 = math.sqrt(sum([x ** 2 for x in indict1_keys_vector]))
        tmp2 = math.sqrt(sum([x ** 2 for x in indict2_keys_vector]))
        num2 = tmp1 * tmp2  # num2=sqrt(a1^2+a2^2+a3^2) * sqrt(b1^2+b2^2+b3^2)

        if num2 == 0:
            return 0
        else:
            return float(num1) / num2



    def getDirectorSimilarity(self, director_imdbids_path):
        with open(director_imdbids_path) as director_imdbids_file:
            director_imdbids_dict = json.loads(director_imdbids_file.readline())

        director_genres_dict = {}
        director_vionelscene_dict = {}
        director_locationcity_dict = {}
        director_locationcountry_dict = {}
        for directorid in director_imdbids_dict:
            movie_list = director_imdbids_dict[directorid]
            genre_num_dict = {}
            vionelscene_num_dict = {}
            locationcity_num_dict = {}
            locationcountry_num_dict = {}

            for movieid in movie_list:
                genre_list = self.imdbid_genre_dict[movieid]
                vionelscene_list = self.imdbid_vionelscene_dict[movieid]
                locationcity_list = self.imdbid_locationcity_dict[movieid]
                locationcountry_list = self.imdbid_locationcountry_dict[movieid]

                for genre in genre_list:
                    if genre not in genre_num_dict.keys():
                        genre_num_dict[genre] = 1
                    else:
                        genre_num_dict[genre] += 1

                for vionelscene in vionelscene_list:
                    if vionelscene not in vionelscene_num_dict.keys():
                        vionelscene_num_dict[vionelscene] = 1
                    else:
                        vionelscene_num_dict[vionelscene] += 1

                for locationcity in locationcity_list:
                    if locationcity not in locationcity_num_dict.keys():
                        locationcity_num_dict[locationcity] = 1
                    else:
                        locationcity_num_dict[locationcity] += 1

                for locationcountry in locationcountry_list:
                    if locationcountry not in locationcountry_num_dict.keys():
                        locationcountry_num_dict[locationcountry] = 1
                    else:
                        locationcountry_num_dict[locationcountry] += 1

            director_genres_dict[directorid] = genre_num_dict
            director_vionelscene_dict[directorid] = vionelscene_num_dict
            director_locationcity_dict[directorid] = locationcity_num_dict
            director_locationcountry_dict[directorid] = locationcountry_num_dict

        director_director_score_dict = {}
        for k1 in director_imdbids_dict:
            for k2 in director_imdbids_dict:
                director_score_dict = {}
                genre_score = self.__getCosSim(director_genres_dict[k1], director_genres_dict[k2])
                vionelscene_score = self.__getCosSim(director_vionelscene_dict[k1], director_vionelscene_dict[k2])
                locationcity_score = self.__getCosSim(director_locationcity_dict[k1], director_locationcity_dict[k2])
                locationcountry_score = self.__getCosSim(director_locationcountry_dict[k1], director_locationcountry_dict[k2])

                score = genre_score + vionelscene_score + locationcity_score + locationcountry_score

                director_score_dict[k2] = score

            director_director_score_dict[k1] = director_score_dict


        print Counter(director_director_score_dict).most_common(20)

        




cf = CoefficientFeature()
cf.getDirectorSimilarity("director_imdbids.json")
