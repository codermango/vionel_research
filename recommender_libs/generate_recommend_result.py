import json
import recommender 


boxer_movies_path = "boxer_movies.json"


def generate_all_recommendatioin():
    all_imdbid_list = []
    with open(boxer_movies_path) as boxer_movies_file, open("recommended_results.json", "w") as recommended_results_file:
        for line in boxer_movies_file:
            movie = json.loads(line)
            imdbid = movie["imdbId"]
            all_imdbid_list.append(imdbid)

        result_dict = {}
        count = 0
        for movieid in all_imdbid_list:
            count += 1
            print count
            recommended_dict_list = recommender.recommend([movieid, movieid], 20)["movie"]
            recommended_list = []
            for item in recommended_dict_list:
                recommended_list.append(item[0])
            result_dict[movieid] = recommended_list

        result_dict_json = json.dumps(result_dict)
        recommended_results_file.write(result_dict_json)


def statics_features():
    all_imdbid_list = []
    with open(boxer_movies_path) as boxer_movies_file, open("statics_features.json", "a") as statics_features_file:
        for line in boxer_movies_file:
            movie = json.loads(line)
            imdbid = movie["imdbId"]
            all_imdbid_list.append(imdbid)

        feature_allscore_dict1 = {}
        feature_allscore_dict1["imdbGenres"] = 0
        feature_allscore_dict1["imdbMainactors"] = 0
        feature_allscore_dict1["imdbDirectors"] = 0
        feature_allscore_dict1["imdbKeywords"] = 0
        feature_allscore_dict1["wikiKeywords"] = 0
        feature_allscore_dict1["vionelThemes"] = 0
        feature_allscore_dict1["vionelScene"] = 0
        feature_allscore_dict1["locationCity"] = 0
        feature_allscore_dict1["locationCountry"] = 0

        feature_allscore_dict2 = {}
        feature_allscore_dict2["imdbGenres"] = 0
        feature_allscore_dict2["imdbMainactors"] = 0
        feature_allscore_dict2["imdbDirectors"] = 0
        feature_allscore_dict2["imdbKeywords"] = 0
        feature_allscore_dict2["wikiKeywords"] = 0
        feature_allscore_dict2["vionelThemes"] = 0
        feature_allscore_dict2["vionelScene"] = 0
        feature_allscore_dict2["locationCity"] = 0
        feature_allscore_dict2["locationCountry"] = 0

        feature_allscore_dict3 = {}
        feature_allscore_dict3["imdbGenres"] = 0
        feature_allscore_dict3["imdbMainactors"] = 0
        feature_allscore_dict3["imdbDirectors"] = 0
        feature_allscore_dict3["imdbKeywords"] = 0
        feature_allscore_dict3["wikiKeywords"] = 0
        feature_allscore_dict3["vionelThemes"] = 0
        feature_allscore_dict3["vionelScene"] = 0
        feature_allscore_dict3["locationCity"] = 0
        feature_allscore_dict3["locationCountry"] = 0

        count = 0
        for movieid in all_imdbid_list:
            count += 1
            print count, movieid
            recommended_dict = recommender.recommend([movieid, movieid], 20)

            recommended_movie_score_dict = dict(recommended_dict["movie"])
            recommended_movie_reason_dict = dict(recommended_dict["reason"])

            # print recommended_movie_score_dict
            # print recommended_movie_reason_dict

            for k, v in recommended_movie_reason_dict.items():
                try:
                    feature_allscore_dict1[v[0]] += 1
                except IndexError:
                    continue

                try:
                    feature_allscore_dict2[v[1]] += 1
                except IndexError:
                    continue

                try:
                    feature_allscore_dict3[v[2]] += 1
                except IndexError:
                    continue

        print feature_allscore_dict1
        print feature_allscore_dict2
        print feature_allscore_dict3
        statics_features_file.write(json.dumps(feature_allscore_dict1) + "\n")
        statics_features_file.write(json.dumps(feature_allscore_dict2) + "\n")
        statics_features_file.write(json.dumps(feature_allscore_dict3) + "\n")



statics_features()


