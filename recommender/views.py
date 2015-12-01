import json
from django.shortcuts import render
from django.http import HttpResponse

from recommender_libs.recommender import SimilarityRecommender


# Create your views here.

def _generate_result_for_show(result_dict):
    recommended_movie_dict = result_dict['movie']
    feature_for_rec_dict = result_dict['reason']

    sorted_recommended_movie_dict = sorted(recommended_movie_dict.iteritems(), key=lambda d:d[1], reverse = True)
    reason_dict = {}
    for movieid, features in feature_for_rec_dict.items():
        # print features # Can watch the score for each feature here.
        sorted_features = sorted(features.iteritems(), key=lambda d:d[1], reverse = True)[:4]

        feature_for_show_list = []
        for feature in sorted_features:
            feature_for_show_list.append(feature[0])

        reason_dict[movieid] = feature_for_show_list
    
    return sorted_recommended_movie_dict, reason_dict.items()


def index(request):
    return render(request, 'recommender/index.html')

def recommend_page(request):
    input_movies = request.GET.get('inputMovies').strip()
    recommend_num = int(request.GET.get('recommendNum'))

    # sr = SimilarityRecommender('tv', 'VionelMovies', 'AllSeries')
    sr = SimilarityRecommender('movie', 'VionelMovies')
    result_dict = sr.recommend([input_movies], 10)

    movies_to_show = {}
    movies_to_show['recommend_tuple_list'], movies_to_show['reason_tuple_list'] = _generate_result_for_show(result_dict)

    movies_to_show['input_movie_list'] = [input_movies]


    return render(request, 'recommender/index.html', {'movies_to_show': movies_to_show})
