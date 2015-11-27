# coding: utf-8
from __future__ import division
import math


def intersection_of_values_for_certain_keys(item_list, item_with_value_dict):
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


def calculate_cosine(indict1, indict2):
    """Calculate cosine of two lists that are generated from the two input dicts.
        
        Example:
            indict1 = {'a':1, 'b':2, 'c':3}
            indict2 = {'b':2, 'c':2, 'd':2}
            The calculation will be like this:
            List  ->  ['a', 'b', 'c', 'd']
            list1 ->  [ 1,   2,   3,   0 ]
            list2 ->  [ 0,   2,   2,   2 ]

            The result will be the cosine of list1 and list2

    """

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


def jsonfile_to_dict(self, json_file_path):
    """Read JSON file and transform to python dict"""

    with open(os.path.split(os.path.realpath(__file__))[0] + json_file_path) as json_file:
        result_dict = json.loads(json_file.readline())
    return result_dict


def union_of_values_for_spec_keys(key_list, input_dict):
    """Example:
        key_list = ['A', 'B']
        input_dict = {
                        'A':[1,2,3],
                        'B':[2,3,4],
                        'C':[4,5,6]
                     }
        Ignore the keys that the input_dict doesn't have.
        Return:
            union([1,2,3] + [2,3,4])
            which is: [1,2,3,4]
    """

    union_values = []
    for item in key_list:
        try:
            values = input_dict[item]
            union_values += values
        except KeyError:
            continue
    union_values = list(set(union_values))

    return union_values









