from py2neo import Graph,Node, Relationship, authenticate


class RecommenderDB_neo4j:

    def __init__(self):
        authenticate("localhost:7474", "neo4j", "mark")
        self.graph = Graph()

    def get_imdbid_feature_dict(self, feature_name):
        result_dict = {}

        imdbid_list = []
        movies = self.graph.cypher.execute("match (movie:movie) return movie.imdbId")
        for movie in movies:
            imdbid_list.append(str(movie[0]))
            
        # print len(imdbid_list)


        feature_key = ""
        flag = ""
        if feature_name == "actor":
            feature_key = "imdbActor"
            flag = "node"
        elif feature_name == "director":
            feature_key = "director"
            flag = "node"
        elif feature_name == "genre":
            feature_key = "genre"
            flag = "node"
        elif feature_name == "language":
            feature_key = "language"
            flag = "node"
        elif feature_name == "imdbkeyword":
            feature_key = "imdbKeyword"
            flag = "node"
        elif feature_name == "wikikeyword":
            feature_key = "wikikeyword"
            flag = "node"
        elif feature_name == "vioneltheme":
            feature_key = "vionelTheme"
            flag = "node"
        elif feature_name == "imdbrating":
            feature_key = "imdbRating"
            flag = "attr"
        elif feature_name == "releaseyear":
            feature_key = "releaseYear"
            flag = "attr"


        
        if flag == "node":
            for imdbid in imdbid_list:
                # node = list(self.graph.find('movie', property_key='imdbId',property_value=imdbid))[0]
                # print node
                # for rel in self.graph.match(start_node=node, rel_type="has_Actor"):
                #     print rel.end_node.properties["name"]

                
                

                feature_list = []
                features = self.graph.cypher.execute("match (movie:movie {imdbId:'" + imdbid + "'}) --> (feature:" + feature_key + ") return feature.name")
                

                # print list(features)

                


                # for feature in features:
                #     print feature
                #     feature_list.append(feature[0])
                # result_dict[imdbid] = feature_list
        elif flag == "attr":
            for imdbid in imdbid_list:
                features = self.graph.cypher.execute("match (movie:movie {imdbId:'" + imdbid + "'}) return movie." + feature_key)

                result_dict[imdbid] = features[0][0]


        return result_dict

        # print movies





rc = RecommenderDB_neo4j()
rc.get_imdbid_feature_dict("actor")
