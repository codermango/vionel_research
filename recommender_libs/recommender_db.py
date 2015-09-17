import pymongo
from pymongo import MongoClient
import json


class RecommenderDB:

    def __init__(self):
        client = MongoClient()
        self.db = client.VionelMovies
        self.boxerMoviesCollection = self.db.boxerMovies
        

    def get_all_feature_list(self, feature_name):
        feature_list = []
        feature_dict_list = self.boxerMoviesCollection.find({}, {feature_name: 1, "_id": 0})
        for feature_dict in feature_dict_list:
            feature_list += feature_dict[feature_name]
        feature_list = list(set(feature_list))
        # print feature_list
        return feature_list


    def get_imdbid_feature_dict(self, feature_name):
        result_dict = {}

        all_movies_feature_dict_list = self.boxerMoviesCollection.find({}, {"imdbId": 1, feature_name: 1, "_id": 0})
        
        for movie in all_movies_feature_dict_list:
            imdbid = movie["imdbId"]
            feature = movie[feature_name]
            result_dict[imdbid] = feature
        # print result_dict
        return result_dict



    def create_feature_num_collection(self):
        genre_dict = self.get_feature_featurenum_dict("imdbGenres")
        actor_dict = self.get_feature_featurenum_dict("imdbActors")
        director_dict = self.get_feature_featurenum_dict("imdbDirectors")
        imdbkeyword_dict = self.get_feature_featurenum_dict("imdbKeywords")
        wikikeyword_dict = self.get_feature_featurenum_dict("wikiKeywords")
        vioneltheme_dict = self.get_feature_featurenum_dict("vionelThemes")
        vionelscene_dict = self.get_feature_featurenum_dict("vionelScene")
        locationcountry_dict = self.get_feature_featurenum_dict("locationCountry")
        locationcity_dict = self.get_feature_featurenum_dict("locationCity")

        result_dict = {}
        result_dict["imdbGenres"] = genre_dict
        result_dict["imdbActors"] = actor_dict
        result_dict["imdbDirectors"] = director_dict
        result_dict["imdbKeywords"] = imdbkeyword_dict
        result_dict["wikiKeywords"] = wikikeyword_dict
        result_dict["vionelThemes"] = vioneltheme_dict
        result_dict["vionelScene"] = vionelscene_dict
        result_dict["locationCountry"] = locationcountry_dict
        result_dict["locationCity"] = locationcity_dict


        with open("feature_num.json", "w") as feature_num_file:
            result_dict_json = json.dumps(result_dict)
            feature_num_file.write(result_dict_json)



# recommenderdb = RecommenderDB()
# recommenderdb.get_imdbid_feature_dict("imdbGenres")
# # recommenderdb.get_all_feature_list("imdbActors")
# recommenderdb.get_feature_featurenum_dict("imdbGenres")
# recommenderdb.create_feature_num_collection()
# recommenderdb.get_movieids_by_feature_dict("imdbActors")