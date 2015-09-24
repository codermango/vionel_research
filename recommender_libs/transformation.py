#!coding=utf-8
import json
import math
from collections import Counter
import os
import recommender




def exchange_key_value_of_dict(input_dict):
    '''此函数作用:
        把{"a": [1, 2, 3], "b": [1, 3, 5]}转化成{1: ["a", "b"], 2: ["a"], 3: ["a", "b"], 5: ["b"]}
    '''
    union_of_input_dict_values = []
    input_dict_values = input_dict.values()

    for k, v in input_dict.items():
        union_of_input_dict_values += v

    union_of_input_dict_values = set(union_of_input_dict_values)
    print len(union_of_input_dict_values)

    output_dict = {}
    for item in union_of_input_dict_values:
        output_value = []
        for k1, v1 in input_dict.items():
            if item in v1:
                output_value.append(k1)
        output_dict[item] = output_value
        print len(output_dict)

    return output_dict



def genreate_feature_imdbids(imdbid_features_dict, generated_file_path):
    feature_imdbids_dict = exchange_key_value_of_dict(imdbid_features_dict)
    feature_imdbids_json = json.dumps(feature_imdbids_dict)
    with open(generated_file_path, "w") as generated_file:
        generated_file.write(feature_imdbids_json)




def transform(all_movies_file_path):

    imdbid_directors_dict = {}
    imdbid_actors_dict = {}
    imdbid_ratings_dict = {}
    imdbid_releaseyear_dict = {}
    imdbid_genres_dict = {}
    imdbid_language_dict = {}
    imdbid_imdbkeywords_dict = {}
    imdbid_wikikeywords_dict = {}
    imdbid_vioneltheme_dict = {}
    imdbid_vionelscene_dict = {}
    imdbid_locationcountry_dict = {}
    imdbid_locationcity_dict = {}
    imdbid_mainactors_dict = {}

    with open(all_movies_file_path) as all_movies_file:
        for line in all_movies_file:
            movie = json.loads(line)
            imdbid = movie["imdbId"]

            imdbid_directors_dict[imdbid] = movie["imdbDirectors"]
            imdbid_actors_dict[imdbid] = movie["imdbActors"]
            imdbid_ratings_dict[imdbid] = movie["imdbRating"]
            imdbid_releaseyear_dict[imdbid] = movie["releaseYear"]
            imdbid_genres_dict[imdbid] = movie["imdbGenres"]
            imdbid_language_dict[imdbid] = movie["language"]
            imdbid_imdbkeywords_dict[imdbid] = movie["imdbKeywords"]
            imdbid_wikikeywords_dict[imdbid] = movie["wikiKeywords"]
            imdbid_vioneltheme_dict[imdbid] = movie["vionelThemes"]
            imdbid_vionelscene_dict[imdbid] = movie["vionelScene"]
            imdbid_locationcity_dict[imdbid] = movie["locationCity"]
            imdbid_locationcountry_dict[imdbid] = movie["locationCountry"]
            imdbid_mainactors_dict[imdbid] = movie["imdbMainactors"]


    # genreate_feature_imdbids(imdbid_directors_dict, "director_imdbids.json")
    # genreate_feature_imdbids(imdbid_actors_dict, "actor_imdbids.json")
    # genreate_feature_imdbids(imdbid_genres_dict, "genre_imdbids.json")
    # genreate_feature_imdbids(imdbid_imdbkeywords_dict, "imdbkeyword_imdbids.json")
    # genreate_feature_imdbids(imdbid_wikikeywords_dict, "wikikeyword_imdbids.json")
    # genreate_feature_imdbids(imdbid_vioneltheme_dict, "vioneltheme_imdbids.json")
    # genreate_feature_imdbids(imdbid_vionelscene_dict, "vionelscene_imdbids.json")
    # genreate_feature_imdbids(imdbid_locationcity_dict, "locationcity_imdbids.json")
    # genreate_feature_imdbids(imdbid_locationcountry_dict, "locationcountry_imdbids.json")
    # genreate_feature_imdbids(imdbid_mainactors_dict, "mainactor_imdbids.json")



###############################################################################################


def generate_movie_information(infile):
    with open(infile) as infile_file, open("boxer_movies_information.dat", "w") as boxer_movies_information_file:
        count = 0
        for line in infile_file:
            count += 1
            print count

            movie = json.loads(line)

            output_dict = {}
            output_dict["imdbGenres"] = movie["genres"]
            output_dict["language"] = movie["language"]
            output_dict["imdbDirectors"] = movie["imdbDirectors"]
            output_dict["imdbKeywords"] = movie["imdbKeywords"]
            output_dict["imdbRating"] = movie["imdbRating"]
            output_dict["imdbActors"] = movie["imdbActors"]
            output_dict["imdbId"] = movie["imdbId"]
            output_dict["releaseYear"] = movie["releaseYear"]
            output_dict["imdbMainactors"] = movie["imdbMainactors"]

            wikikeyword_list = []
            for item in movie["wikikeywords"]:
                wikikeyword_list.append(item["keywordWikiId"])

            vioneltheme_list = []
            for theme in movie["vionelThemes"]:
                vioneltheme_list.append(theme["vionelThemeID"])

            locationcountry_list = movie["locationCountry"].values() + movie["locationCity"].values() + movie["locationState"].values()
            locationcity_list = movie["locationCity"].keys() + movie["locationState"].keys()
            vionelscene_list = movie["vionScene"].keys()

            locationcountry_list = list(set(locationcountry_list))
            locationcity_list = list(set(locationcity_list))

            print locationcountry_list
            print locationcity_list
            print vionelscene_list
            print


            output_dict["wikiKeywords"] = wikikeyword_list
            output_dict["vionelThemes"] = vioneltheme_list
            output_dict["locationCountry"] = locationcountry_list
            output_dict["locationCity"] = locationcity_list
            output_dict["vionelScene"] = vionelscene_list

            output_json = json.dumps(output_dict)
            boxer_movies_information_file.write(output_json + "\n")




def createweight():
    movie_list = []
    feature_maxscore_dict = {}

    actor_score_list = []
    director_score_list = []
    genre_score_list = []
    imdbkeyword_score_list = []
    wikikeyword_score_list = []
    vioneltheme_score_list = []


    with open("boxer_movies_information.dat") as boxer_movies_information_file:
        for line in boxer_movies_information_file:
            movie = json.loads(line)
            imdbid = movie["imdbId"]
            movie_list.append(imdbid)
            
        max_actorscore = 0
        max_directorscore = 0
        max_genrescore = 0
        max_imdbkeywordscore = 0
        max_wikikeywordscore = 0
        max_vionelthemescore = 0

    count = 0

    for imdbid in movie_list:
        feature_counter_dict = recommender.getallsimscore([imdbid, imdbid])
        actorscore = max(dict(feature_counter_dict["imdb_actor"]).values())
        directorscore = max(dict(feature_counter_dict["imdb_director"]).values())
        genrescore = max(dict(feature_counter_dict["imdb_genre"]).values())
        imdbkeywordscore = max(dict(feature_counter_dict["imdb_keyword"]).values())
        wikikeywordscore = max(dict(feature_counter_dict["wiki_keyword"]).values())
        vionelthemescore = max(dict(feature_counter_dict["vionel_theme"]).values())

        # if max_actorscore < actorscore:
        #     max_actorscore = actorscore
        # elif max_directorscore < directorscore:
        #     max_directorscore = directorscore
        # elif max_genrescore < genrescore:
        #     max_genrescore = genrescore
        # elif max_imdbkeywordscore < imdbkeywordscore:
        #     max_imdbkeywordscore = imdbkeywordscore
        # elif max_wikikeywordscore < wikikeywordscore:
        #     max_wikikeywordscore = wikikeywordscore
        # elif max_vionelthemescore < vionelthemescore:
        #     max_vionelthemescore = vionelthemescore


        actor_score_list.append(actorscore)
        director_score_list.append(directorscore)
        genre_score_list.append(genrescore)
        imdbkeyword_score_list.append(imdbkeywordscore)
        wikikeyword_score_list.append(wikikeywordscore)
        vioneltheme_score_list.append(vionelthemescore)

        count += 1
        print count
        # print max_genrescore
        # print max_actorscore
        # print max_directorscore
        # print max_imdbkeywordscore
        # print max_wikikeywordscore
        # print max_vionelthemescore
        # print 
        print genrescore
        print actorscore
        print directorscore
        print imdbkeywordscore
        print wikikeywordscore
        print vionelthemescore
        print 


    print sum(actor_score_list) / len(actor_score_list)
    print sum(director_score_list) / len(director_score_list)
    print sum(genre_score_list) / len(genre_score_list)
    print sum(imdbkeyword_score_list) / len(imdbkeyword_score_list)
    print sum(wikikeyword_score_list) / len(wikikeyword_score_list)
    print sum(vioneltheme_score_list) / len(vioneltheme_score_list)

    # feature_maxscore_dict["imdbActor"] = max_actorscore
    # feature_maxscore_dict["imdbDirector"] = max_directorscore
    # feature_maxscore_dict["imdbGenre"] = max_genrescore
    # feature_maxscore_dict["imdbKeyword"] = max_genrescore
    # feature_maxscore_dict["wikiKeyword"] = max_wikikeywordscore
    # feature_maxscore_dict["vionelTheme"] = max_vionelthemescore

    # print feature_maxscore_dict








generate_movie_information("boxer_movies.json")
# transform("boxer_movies_information.dat")

# createweight()

