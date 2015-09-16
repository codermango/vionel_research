import pymongo
from pymongo import MongoClient


class RecommenderDB:
    db = None
    collection = None

    def __init__(self):
        client = MongoClient()
        self.db = client.VionelMovies
        self.collection = self.db.boxerMovies

    def get_imdbid_feature_dict(self, feature_name):
        result_dict = {}

        all_movies_list = list(self.collection.find({}, {"imdbId": 1, feature_name: 1, "_id": 0}))
        # print all_movies_list
        for movie in all_movies_list:
            imdbid = movie["imdbId"]
            feature = movie[feature_name]
            result_dict[imdbid] = feature
        return result_dict

# recommenderdb = RecommenderDB()
# recommenderdb.get_imdbid_feature_dict("actor")