import json


with open("boxer_movies.json") as boxer_movies_file:
    for line in boxer_movies_file:
        movie = json.loads(line)
        locationcity_list = movie["locationCity"].keys()
        new_locationcity_list = []
        for city in locationcity_list:
            if city.find(".") != -1:
                city = city.replace(".", "")
                print city