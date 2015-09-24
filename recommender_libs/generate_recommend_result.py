import json
import recommender 


all_imdbid_list = []
with open("boxer_movies.json") as boxer_movies_file, open("recommended_results.json", "w") as recommended_results_file:
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
