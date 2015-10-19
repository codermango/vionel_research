#!coding=utf-8
import json
import math
from recommender_helper import RecommenderHelper
from recommender_db import RecommenderDB

from collections import Counter
import os


# recommenderdb = RecommenderDB_neo4j()
recommenderdb = RecommenderDB()

def filter_by_rating_and_releaseyear(combined_movieid_sim_counter):

    movieid_imdbrating_dict = recommenderdb.get_imdbid_feature_dict("imdbRating")
    movieid_releaseyear_dict = recommenderdb.get_imdbid_feature_dict("releaseYear")

    for item in combined_movieid_sim_counter:
        try:
            # combined_movieid_sim_counter[item] *= movieid_imdbrating_dict[item]
            if movieid_releaseyear_dict[item] < 1990:
                combined_movieid_sim_counter[item] *= 0.6
            elif movieid_releaseyear_dict[item] >= 1990 and movieid_releaseyear_dict[item] < 2000:
                combined_movieid_sim_counter[item] *= 0.7
            elif movieid_releaseyear_dict[item] >= 2000 and movieid_releaseyear_dict[item] < 2010:
                combined_movieid_sim_counter[item] *= 0.8
            elif movieid_releaseyear_dict[item] >= 2010 and movieid_releaseyear_dict[item] < 2020:
                combined_movieid_sim_counter[item] *= 0.9
        except KeyError:
            combined_movieid_sim_counter[item] * 0.5
            
    return combined_movieid_sim_counter


def filter_by_language(input_movieid_list, combined_movieid_sim_counter):

    imdbid_language_dict = recommenderdb.get_imdbid_feature_dict("language")

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


def reason_of_recommendation(all_feature_counter_list):
    reason_tuple_list = []
    score_dict = {}
    for key in all_feature_counter_list[0]:
        imdbid = key[0]
        score_dict["imdbGenres"] = all_feature_counter_list[1][imdbid]
        score_dict["imdbMainactors"] = all_feature_counter_list[2][imdbid]
        score_dict["imdbDirectors"] = all_feature_counter_list[3][imdbid]
        score_dict["imdbKeywords"] = all_feature_counter_list[4][imdbid]
        score_dict["wikiKeywords"] = all_feature_counter_list[5][imdbid]
        score_dict["vionelThemes"] = all_feature_counter_list[6][imdbid]
        score_dict["vionelScene"] = all_feature_counter_list[7][imdbid]
        score_dict["locationCity"] = all_feature_counter_list[8][imdbid]
        score_dict["locationCountry"] = all_feature_counter_list[9][imdbid]
        score_dict["RGB"] = all_feature_counter_list[10][imdbid]
        score_dict["Brightness"] = all_feature_counter_list[11][imdbid]
        sorted_score_dict = sorted(score_dict.iteritems(), key=lambda d:d[1], reverse=True)
        reason_list = []
        # print sorted_score_dict
        for item in sorted_score_dict[:4]:
            if item[1] != 0:
                reason_list.append(item[0])
        reason_tuple_list.append((key[0], reason_list,))
    return reason_tuple_list


def multiply_coefficient(movieid_score_counter, coefficient):
    result_count = Counter()
    for k, v in movieid_score_counter.items():
        result_count[k] = v * coefficient
    return result_count

def recommend(input_movieid_list, num_of_recommended_movies):

    # 以下可分别得到根据genre和mawid推荐出的结果，均为（movied_id: cos_sim_value）这种的字典
    recommender_helper = RecommenderHelper()
    imdbdirector_movieid_sim_dict = recommender_helper.recommend(input_movieid_list, "imdbDirectors")
    imdbgenre_movieid_sim_dict = recommender_helper.recommend(input_movieid_list, "imdbGenres")
    imdbkeyword_movieid_sim_dict = recommender_helper.recommend(input_movieid_list, "imdbKeywords")
    wikikeyword_movieid_sim_dict = recommender_helper.recommend(input_movieid_list, "wikiKeywords")
    vioneltheme_movieid_sim_dict = recommender_helper.recommend(input_movieid_list, "vionelThemes")
    vionelscene_movieid_sim_dict = recommender_helper.recommend(input_movieid_list, "vionelScene")
    locationcountry_movieid_sim_dict = recommender_helper.recommend(input_movieid_list, "locationCountry")
    locationcity_movieid_sim_dict = recommender_helper.recommend(input_movieid_list, "locationCity")
    imdbmainactor_movieid_sim_dict = recommender_helper.recommend(input_movieid_list, "imdbMainactors")
    rgb_movieid_sim_dict = recommender_helper.recommend(input_movieid_list, "RGB")
    brightness_movieid_sim_dict = recommender_helper.recommend(input_movieid_list, "Brightness")

    imdbgenre_movieid_sim_counter = Counter(imdbgenre_movieid_sim_dict)
    imdbdirector_movieid_sim_counter = Counter(imdbdirector_movieid_sim_dict)
    imdbkeyword_movieid_sim_counter = Counter(imdbkeyword_movieid_sim_dict)
    wikikeyword_movieid_sim_counter = Counter(wikikeyword_movieid_sim_dict)
    vioneltheme_movieid_sim_counter = Counter(vioneltheme_movieid_sim_dict)
    vionelscene_movieid_sim_counter = Counter(vionelscene_movieid_sim_dict)
    locationcountry_movieid_sim_counter = Counter(locationcountry_movieid_sim_dict)
    locationcity_movieid_sim_counter = Counter(locationcity_movieid_sim_dict)
    imdbmainactor_movieid_sim_counter = Counter(imdbmainactor_movieid_sim_dict)
    rgb_movieid_sim_counter = Counter(rgb_movieid_sim_dict)
    brightness_movieid_sim_counter = Counter(brightness_movieid_sim_dict)


    locationcountry_movieid_sim_counter = multiply_coefficient(locationcountry_movieid_sim_counter, 0.3)
    vionelscene_movieid_sim_counter = multiply_coefficient(vionelscene_movieid_sim_counter, 0.35)
    locationcity_movieid_sim_counter = multiply_coefficient(locationcity_movieid_sim_counter, 0.5)
    imdbgenre_movieid_sim_counter = multiply_coefficient(imdbgenre_movieid_sim_counter, 0.5)
    imdbdirector_movieid_sim_counter = multiply_coefficient(imdbdirector_movieid_sim_counter, 0.7)
    imdbmainactor_movieid_sim_counter = multiply_coefficient(imdbmainactor_movieid_sim_counter, 0.9)
    imdbkeyword_movieid_sim_counter = multiply_coefficient(imdbkeyword_movieid_sim_counter, 0.6)
    wikikeyword_movieid_sim_counter = multiply_coefficient(wikikeyword_movieid_sim_counter, 1.3)
    vioneltheme_movieid_sim_counter = multiply_coefficient(vioneltheme_movieid_sim_counter, 1.3)
    rgb_movieid_sim_counter = multiply_coefficient(rgb_movieid_sim_counter, 0.25)
    brightness_movieid_sim_counter = multiply_coefficient(brightness_movieid_sim_counter, 0.25)

    combined_movieid_sim_counter = imdbgenre_movieid_sim_counter + imdbmainactor_movieid_sim_counter + imdbdirector_movieid_sim_counter + imdbkeyword_movieid_sim_counter + wikikeyword_movieid_sim_counter + vioneltheme_movieid_sim_counter + vionelscene_movieid_sim_counter + locationcountry_movieid_sim_counter + locationcity_movieid_sim_counter + rgb_movieid_sim_counter + brightness_movieid_sim_counter

    # combined_movieid_sim_counter = imdbgenre_movieid_sim_counter + wikikeyword_movieid_sim_counter + vioneltheme_movieid_sim_counter + vionelscene_movieid_sim_counter + rgb_movieid_sim_counter + brightness_movieid_sim_counter

    for key in input_movieid_list:
        del combined_movieid_sim_counter[key]
        del imdbgenre_movieid_sim_counter[key]
        del imdbdirector_movieid_sim_counter[key]
        del imdbkeyword_movieid_sim_counter[key]
        del wikikeyword_movieid_sim_counter[key]
        del vioneltheme_movieid_sim_counter[key]
        del vionelscene_movieid_sim_counter[key]
        del locationcity_movieid_sim_counter[key]
        del locationcountry_movieid_sim_counter[key]
        del imdbmainactor_movieid_sim_counter[key]
        del rgb_movieid_sim_counter[key]
        del brightness_movieid_sim_counter[key]


    

    # filter
    # 乘上rating和releaseYear产生的系数
    # combined_movieid_sim_counter = filter_by_rating_and_releaseyear(combined_movieid_sim_counter)
    combined_movieid_sim_counter = filter_by_language(input_movieid_list, combined_movieid_sim_counter)

    final_co_recommended_movies = combined_movieid_sim_counter.most_common(num_of_recommended_movies)

    # get the features that have the top two scores.
    all_feature_counter_list = [final_co_recommended_movies, imdbgenre_movieid_sim_counter, imdbmainactor_movieid_sim_counter, imdbdirector_movieid_sim_counter, imdbkeyword_movieid_sim_counter, wikikeyword_movieid_sim_counter, vioneltheme_movieid_sim_counter, vionelscene_movieid_sim_counter, locationcity_movieid_sim_counter, locationcountry_movieid_sim_counter, rgb_movieid_sim_counter, brightness_movieid_sim_counter]

    reason_tuple_list = reason_of_recommendation(all_feature_counter_list)

    # print reason_tuple_list
    result_dict = dict()
    result_dict["movie"] = final_co_recommended_movies
    result_dict["reason"] = reason_tuple_list

    return result_dict


###########################################################################
###########################################################################






