import json

needed_movies_list = []
with open("needed_movies.txt") as needed_movies_file:
    for needed_movies_line in needed_movies_file:
        needed_movies_list.append(needed_movies_line.strip())

new_all10_movies_dict = {}
with open("new_all10_movies.json") as new_all10_movies_file:
    for new_all10_movies_line in new_all10_movies_file:
        new_all10_movie = json.loads(new_all10_movies_line)
        new_all10_movies_dict[new_all10_movie["imdbid"]] = new_all10_movie

imdbid_vionelid_dict = {}
with open("reconciled_boxer.jl") as imdbid_vionelid_file:
    for imdbid_vionelid_line in imdbid_vionelid_file:
        imdbid_vionelid = json.loads(imdbid_vionelid_line)
        imdbid_vionelid_dict[imdbid_vionelid["imdbID"]] = imdbid_vionelid["vionelID"]

imdbid_wikikeyword_dict = {}
with open("wikikeywords.txt") as imdbid_wikikeyword_file:
    for imdbid_wikikeyword_line in imdbid_wikikeyword_file:
        imdbid_wikikeyword = json.loads(imdbid_wikikeyword_line)
        imdbid_wikikeyword_dict[imdbid_wikikeyword["imdbId"]] = imdbid_wikikeyword["wikiKeywords"]

count = 0
with open("added_movie.txt", "w") as added_movie_file:
    for imdbid in needed_movies_list:
        count += 1
        print count

        try:
            movie = new_all10_movies_dict[imdbid]
        except KeyError:
            continue
        # print movie

        movie["imdbId"] = movie["imdbid"]
        del movie["imdbid"]

        movie["imdbKeywords"] = movie["keywords"]
        del movie["keywords"]

        movie["vionelID"] = imdbid_vionelid_dict[movie["imdbId"]]

        try:
            movie["wikikeywords"] = imdbid_wikikeyword_dict[movie["imdbId"]]
        except KeyError:
            pass
        movie_json = json.dumps(movie)
        added_movie_file.write(movie_json + "\n")





















