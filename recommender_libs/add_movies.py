import json



new_movie_dict = {}
with open("reconciled_boxer.jl") as new_movie_file:
    for new_line in new_movie_file:
        new_movie = json.loads(new_line)
        new_movie_dict[new_movie["imdbID"]] = new_movie["vionelID"]

exist_boxer_movie_list = []
with open("boxer_movies.json") as boxer_movies_file:
    for boxer_movies_line in boxer_movies_file:
        boxer_movie = json.loads(boxer_movies_line)
        exist_boxer_movie_list.append(boxer_movie["imdbId"])


needed_movie_list = []
with open("needed_movies.json", "w") as needed_movies_file:
    for item in new_movie_dict.keys():
        if item not in exist_boxer_movie_list:
            needed_movie_list.append(item)


all3_movie_list = []
with open("all3_movies.dat") as all3_movies_file:
    for all3_movies_line in all3_movies_file:
        all3_movie = json.loads(all3_movies_line)
        all3_movie_list.append(all3_movie["imdbId"])

print len(set(all3_movie_list).intersection(set(needed_movie_list)))
