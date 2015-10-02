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


print len(new_movie_dict.keys())
print len(set(new_movie_dict.keys()))

with open("needed_movies.json", "w") as needed_movies_file:
    needed_movie_list = []
    for item in new_movie_dict.keys():
        if item not in exist_boxer_movie_list:
            needed_movie_list.append(item)




with open("all10_movies.dat") as all10_movies_file:
    pass
