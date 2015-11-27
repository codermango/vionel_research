from pymongo import MongoClient


class MongoManager(object):

    def __init__(self, db_name='VionelMovies', collection_name='BoxerMovies', hostname='172.17.42.1', port=27017, username="", password=""):
        self.db_name = db_name
        self.collection_name = collection_name
        self.hostname = hostname
        self.port = port

        self.client = MongoClient(hostname, port)
        if (username != ""):
            admin_db = self.client["admin"]
            admin_db = admin_db.authenticate(username, password)

        self.db = self.client[self.db_name]
        self.collection = self.db[collection_name]

    def close(self):
        self.connection.close()


    def exec_query(self, query, projection):
        result_list = []
        result = self.collection.find(query, projection)
        for item in result:
            result_list.append(item)
        return result_list


if __name__ == '__main__':
    mm = MongoManager('VionelMovies', 'BoxerMovies', '172.17.42.1', 27017, '', '')
    print mm.exec_query({'imdbId': 'tt0482088'}, {"imdbId": 1, 'imdbGenres': 1, "_id": 0})
    # print mm.get_imdbid_feature_dict('imdbDirectors')
