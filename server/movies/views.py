from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Crew, Movie, Similarity
from movies.serializers import MovieSerializer, MovieListSerializer, CrewSerializer, SimilaritySerializer
# Create your views here.

# '/'
# Home 페이지 로드 시 요청받음 
# 영화에 해당하는 reviews 를 prefetch 하여 함께 응답으로 반환 (평균 평점 계산을 위함)
@api_view(['GET'])
def movie_list(request):
    movies = Movie.objects\
        .prefetch_related('reviews')
    
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)

# <int:movie_pk>/
# MovieDetail 페이지 로드 시 요청받음
# 영화 상세 정보를 genres, crews, keywords, 그리고 비슷한 영화까지 응답으로 반환.
@api_view(['GET'])
def movie_detail(request, movie_pk):
    movies = Movie.objects\
                .prefetch_related('genres')\
                .prefetch_related('crews')\
                .prefetch_related('keywords')

    movie = get_object_or_404(movies, pk=movie_pk)

    similarity = Similarity.objects\
                    .filter(source=movie_pk)\
                    .select_related('target')

    m_serializer = MovieSerializer(movie)
    s_serializer = SimilaritySerializer(similarity, many=True)
    return Response({
        'movie': m_serializer.data,
        'similar_movies': s_serializer.data,
    })

# movies/search/
# SearchResult 에서 searchInput 데이터를 보내면, 이 함수에서 데이터베이스 검색 결과를 응답으로 반환.
@api_view(['GET'])
def movie_search(request):
    input_word = request.GET.get('searchInput')

    # Movie 데이터에서 검색어를 기준으로 filter
    searchedMovies = Movie.objects.filter(Q(title__contains=input_word) | Q(original_title__contains=input_word))
    movie_serializer = MovieSerializer(searchedMovies, many=True)
    # Crew 데이터에서 검색어를 기준으로 filter
    searchedCrews = Crew.objects.filter(name__contains=input_word)
    crew_serializer = CrewSerializer(searchedCrews, many=True)

    return Response({
        'movie_data': movie_serializer.data,
        'crew_data': crew_serializer.data,
    })


# (사용안함) => 출연/제작 검색 함수 
# @api_view(['GET'])
# def crew_search(request):
#     input_word = request.GET.get('searchInput')
#     searchedCrews = Crew.objects.filter(title__contains=input_word)
#     serializer = CrewSerializer(searchedCrews, many=True)
#     return Response(serializer.data)

# (사용안함) => 보고싶어요, 보는중, 관심없어요 기능을 위해 작성한 함수.
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def add_playlist(request, movie_pk):
    
#     Playlist.objects.create(
#         p_user=request.user.pk, 
#         p_movie=movie_pk, 
#         status= request.data.status
#     ) 
    
#     movie = get_object_or_404(Movie, pk=movie_pk)
#     like_counter = movie.like_users.count()

#     return Response({
#         'p_user' : movie_pk,
#         'p_movie' : request.user.pk,
#         'status': request.data.status,
#         'success': True,
#         'likeCounter': like_counter,
#     })