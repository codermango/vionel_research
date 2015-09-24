from django.shortcuts import render
from django.http import HttpResponse

from recommender_libs import recommender


# Create your views here.

def index(request):
    return render(request, 'recommender/index.html')

def recommend_page(request):
    input_movies = request.GET.get('inputMovies')
    recommend_num = int(request.GET.get('recommendNum'))

    input_movie_list = input_movies.split(',')
    if len(input_movie_list) == 1:
        input_movie_list.append(input_movie_list[0])
    trimed_movie_list = map(lambda x: x.strip(), input_movie_list)

    result_dict = recommender.recommend(trimed_movie_list, recommend_num)

    movie_score_dict = result_dict["movie"]
    movie_reason_dict = result_dict["reason"]

    movies_to_show = {}
    movies_to_show['input_movie_list'] = trimed_movie_list
    movies_to_show['recommend_tuple_list'] = movie_score_dict
    movies_to_show['reason_tuple_list'] = movie_reason_dict

    return render(request, 'recommender/index.html', {'movies_to_show': movies_to_show})
