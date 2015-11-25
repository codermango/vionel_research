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

            recommended_dict_list = recommender.recommend([movieid], 20)
            recommended_movie_dict_list = recommended_dict_list["movie"]
            recommended_reason_dict_list = recommended_dict_list["reason"]
            recommended_reason_dict = dict(recommended_reason_dict_list)


            recommendation_list = []
            for item in recommended_movie_dict_list:
                recommended_id = item[0]
                recommended_score = item[1]
                
                recommended_movie_list_item = {}
                recommended_movie_list_item["imdbid"] = recommended_id
                recommended_movie_list_item["score"] = recommended_score

                reason_list = recommended_reason_dict[recommended_id]
                # print reason_list
                recommended_movie_list_item["reason"] = []
                for reason in reason_list:
                    if reason == "wikiKeywords":
                        reason = "keywords2"
                    else:
                        reason = reason.replace("imdb", "")
                    recommended_movie_list_item["reason"].append(reason)

                # print recommended_movie_list_item["reason"]



                recommendation_list.append(recommended_movie_list_item)
            
            result_dict[movieid] = recommendation_list

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


def add_recommendation_to_movieprofile():
    with open("recommended_results.json") as recommended_results_file:
        recommended_results_dict = json.loads(recommended_results_file.readline())

    with open("/home/mark/Projects/vionel_research_page/vionfacts/app/data/tt0443543.json") as movie_file:
        movie_dict = json.loads(movie_file.readline())

    imdbid = movie_dict["Imdbid"]
    movie_dict["recommendation"] = recommended_results_dict[imdbid]
    movie_json = json.dumps(movie_dict)

    with open("/home/mark/Projects/vionel_research_page/vionfacts/app/data/new.json", "w") as new_file:
        new_file.write(movie_json)



# statics_features()
generate_all_recommendatioin()
# add_recommendation_to_movieprofile()


