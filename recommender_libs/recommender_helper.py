#!coding=utf-8
from __future__ import division
import json
import math
import os

from recommender_db import RecommenderDB


class RecommenderHelper:

    def __init__(self):
        with open(os.path.split(os.path.realpath(__file__))[0] + "/feature_num.json") as feature_num_file:
            self.feature_num_dict = json.loads(feature_num_file.readline())


    def __jsonfile_to_dict(self, json_file_path):
        json_file = open(os.path.split(os.path.realpath(__file__))[0] + json_file_path)
        result_dict = json.loads(json_file.readline())
        return result_dict

    def __intersection_of_values_for_certain_keys(self, item_list, item_with_value_dict):
        """把一个字典中指定key的value出现次数。

        此函数的作用是，根据item_list中的item从item_with_value找出对应value，统计出这些value的次数，剔除只出现一次的情况。

        Args:
            item_list: item_with_value_dict中需要查找的key的列表。
            item_with_value_dict: 需要遍历的字典，找出对应的value，这些value是结果中的key。

        Returns:
            一个字典，key为item_with_value_dict中对应的value，value出现的次数。
            例子：
                item_list = [id1, id2, id3]
                item_with_value_dict = {id1: [actor1, actor2],
                                        id2: [actor2, actor3],
                                        id3: [actor5, actor1],
                                        id4: [actor1, actor7]}
                最后结果：{actor1: 2, actor2: 2}
        """

        result_dict = {}
        value_list = []

        for item in item_list:
            try:
                value_list += item_with_value_dict[item]
            except KeyError:
                continue

        value_set_list = list(set(value_list))
        for value in value_set_list:
            num_of_value = value_list.count(value)
            # if num_of_value > 1:
            result_dict[value] = num_of_value

        return result_dict


    def __calculate_cosine(self, indict1, indict2):
        
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



    def __comparison_score(self, movieid_list, movieid_with_featureid_dict, coefficient):
        input_movie_features = []
        for item in movieid_list:
            try:
                feature_list = movieid_with_featureid_dict[item]
                input_movie_features += feature_list
            except KeyError:
                continue
        input_movie_features = list(set(input_movie_features))

        result_dict = {}
        for k, v in movieid_with_featureid_dict.items():
            intersection_num = len(list(set(v).intersection(set(input_movie_features))))
            score = intersection_num * coefficient
            if score > 1:
                score = 1
            result_dict[k] = score

        return result_dict



    def recommend(self, movieid_list, recommended_by):
        recommenderdb = RecommenderDB()

        movieid_with_featureid_dict = {}
        featureid_with_movieid_dict = {}

        input_featureid_with_number_dict = {}

        movieid_with_featureid_dict = recommenderdb.get_imdbid_feature_dict(recommended_by)

        # print recommended_by
        result_dict = {}
        if recommended_by == "imdbDirectors" or recommended_by == "imdbGenres" or recommended_by == "locationCountry" or recommended_by == "locationCity" or recommended_by == "vionelScene" or recommended_by == "imdbMainactors" or recommended_by == "RGB" or recommended_by == "Brightness":
            # print movieid_list
            input_featureid_with_number_dict = self.__intersection_of_values_for_certain_keys(movieid_list, movieid_with_featureid_dict)

            all_featureid_list = input_featureid_with_number_dict.keys()

            for k, v in movieid_with_featureid_dict.items():
                intersection_list = list(set(v).intersection(set(all_featureid_list)))
                if not intersection_list:
                    result_dict[k] = 0
                    continue

                compared_movie_feature_num_dict = self.__intersection_of_values_for_certain_keys([k], movieid_with_featureid_dict)

                cosine_score = self.__calculate_cosine(input_featureid_with_number_dict, compared_movie_feature_num_dict)

                result_dict[k] = cosine_score

            return result_dict
        else:
            result_dict = self.__comparison_score(movieid_list, movieid_with_featureid_dict, 0.1)
            return result_dict






