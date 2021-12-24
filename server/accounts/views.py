from django.shortcuts import get_object_or_404
from django.db.models import F,  Q
from django.core.serializers.json import DjangoJSONEncoder

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from movies.models import Movie, Similarity
from movies.serializers import MovieListSerializer
from .serializers import UserSerializer
from .models import User
import json
from itertools import chain


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def signup(request):
#     password1 = request.data.get('password1')
#     password2 = request.data.get('password2')

#     if User.objects.filter(username=request.data.get('username')).exists():
#         return Response({ 'error': '이미 존재하는 사용자 이름입니다.' }, status=status.HTTP_400_BAD_REQUEST)

#     if password1 != password2:
#         return Response({ 'error': '두 비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid(raise_exception=True):
#         user = serializer.save()
#         user.set_password(password1)
#         user.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# Create your views here.
@api_view(['GET'])
def user_profile(request, user_pk):
    # 유저 자기자신이 아닌, 다른 유저의 정보 페이지에서 필요한 정보를 응답 데이터로 반환

    # 유저의 reviews 와 comments 를 prefetch 
    users = User.objects\
            .prefetch_related('reviews')\
            .prefetch_related('comments')

    user = get_object_or_404(users, pk=user_pk)
    user_serializer= UserSerializer(user)

    # 유저가 작성한 리뷰에 해당되는 영화 정보를 가져오기 위해 movie_ids 에 movie id 저장 
    movie_ids = []
    for review in user_serializer.data['reviews']:
        movie_ids.append(review['movie'])

    movies = Movie.objects.filter(pk__in=movie_ids)
    movie_serializer = MovieListSerializer(movies, many=True)

    return Response({
        'user_data' : user_serializer.data,
        'user_moviedata' : movie_serializer.data
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def myprofile(request):
    # 유저 자기자신의 프로필 정보를 응답 데이터로 반환합니다. 

    # 유저의 reviews 와 comments 를 prefetch 
    users = User.objects\
            .prefetch_related('reviews')\
            .prefetch_related('comments')

    # 현재 요청을 보낸 유저를 찾아서 serialize
    user = get_object_or_404(users, pk=request.user.pk)
    user_serializer= UserSerializer(user)

    # 유저가 평가한 영화와 비슷한 영화 상위 5개를 반환하는 로직 
    
    # 1. 사용자의 리뷰데이터에서, 영화 id 를 가져와서 저장 
    movie_ids = [] 
    for review in user_serializer.data['reviews']:
        movie_ids.append(review['movie'])

    # 사용자의 평점과 유사도의 곱을 계산할 때 사용할 함수 
    def getScore(now_rating, similarity):
        return now_rating * similarity

    topFiveResult = [] # 최종 결과 리스트 
    # 2. 사용자의 모든 리뷰를 interate 하면서 유사도 상위 5개 영화를 topFiveResult 에 차례대로 저장  
    for review in user_serializer.data['reviews']:
        movie_id = review['movie']
        now_rating = review['rating']
        topFive = Similarity.objects\
            .filter(source = movie_id)\
            .exclude(target__in = movie_ids)\
            .order_by('-similarity')[:5]\
            .annotate(score=getScore(now_rating, F('similarity'))).values()

        # json_data = json.dumps(list(topFive), cls=DjangoJSONEncoder)
        topFiveResult.append(topFive)

    # 3. 저장된 상위 5개 영화의 모든 집합을 score 기준으로 정렬 
    result_list = sorted(
        chain(*topFiveResult),
        key=lambda x: x['score'], reverse=True)[:20]
    
    # 정렬된 추천 영화 id 데이터(리스트) 를 json 파일로 변환 
    final_data = json.dumps(result_list, cls=DjangoJSONEncoder)

    # score 기준으로 정렬된 리스트에서 영화 상세 정보를 가져오긴 위해 target_id 를 이용 
    target_ids = []
    for result in result_list:
        target_ids.append(result['target_id'])
    
    # 추천 영화 상세 정보 serialize
    r_movies = Movie.objects.filter(pk__in=target_ids)
    r_movie_seriazlier = MovieListSerializer(r_movies, many=True)

    # 유저가 본 영화 상세 정보 serialize
    movies = Movie.objects.filter(pk__in=movie_ids)
    movie_serializer = MovieListSerializer(movies, many=True)

    # 응답
    return Response({
        'user_data' : user_serializer.data,
        'user_moviedata' : movie_serializer.data,
        'user_recommendation': final_data,
        'r_movies': r_movie_seriazlier.data,
    })