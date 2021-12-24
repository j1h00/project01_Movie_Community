from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.conf import settings

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from .models import Review, Comment, Movie
from .serializers import ReviewSerializer, CommentSerializer

# 모든 리뷰를 응답으로 반환 
# @api_view(['GET'])
# def review_list_all(request):
#     reviews = Review.objects.all()
#     serializer = ReviewSerializer(reviews, many=True)
#     return Response(serializer.data)


# 'myreview/<int:movie_pk>/'
# 영화 상세정보 헤더(MovieDetailHeade) 에서 요청
# 그 영화에 해당하는 request.user 의 리뷰를 응답으로 반환 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_review_by_movie(request, movie_pk):
    user = get_object_or_404(get_user_model(), pk=request.user.pk)
    review = user.reviews.filter(movie=movie_pk)
    serializer = ReviewSerializer(review, many=True)
    return Response(serializer.data)


# 'bymovie/<int:movie_pk>/'
# 영화 상세 정보에서 요청
# 영화에 해당하는 모든 리뷰를 응답으로 반환 
@api_view(['GET'])
def review_list_by_movie(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    reviews = movie.reviews.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

# (사용안함)
# UserProfile 에서 요청 
# User 에 해당하는 모든 리뷰를 응답으로 반환
# @api_view(['GET'])
# def review_list_by_user(request, user_pk):
#     user = get_object_or_404(get_user_model(), pk=user_pk)
#     reviews = user.reviews.all()
#     serializer = ReviewSerializer(reviews, many=True)
#     return Response(serializer.data)


# review 생성 시 요청
# 생성된 리뷰를 응답으로 반환 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def review_create(request, movie_pk):
    serializer = ReviewSerializer(data=request.data)
    movie = get_object_or_404(Movie, pk=movie_pk)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, movie=movie) # 추후수정
        return Response(serializer.data)


# ReviewDetail 에서 상세 조회 시 요청
# 리뷰 상세 정보를 응답으로 반환 
@api_view(['GET'])
def review_detail(request, review_pk):
    reviews = Review.objects\
            .prefetch_related('user')\
            .prefetch_related('movie')

    review = get_object_or_404(reviews, pk=review_pk)
    serializer = ReviewSerializer(review)
    return Response(serializer.data)

# review 수정 삭제 시 요청 
# 리뷰 상세 정보 혹은 delete success 메시지를 응답으로 반환 
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def review_update_or_delete(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)

    # update article
    if request.method == 'PUT':
        serializer = ReviewSerializer(data=request.data, instance=review)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    # delete article
    else:
        review.delete()
        return Response('delete success', status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET'])
# def comment_list_by_user(request, user_pk):
#     user = get_object_or_404(get_user_model(), pk=user_pk)
#     comment = user.comments.all()
#     serializer = CommentSerializer(comment, many=True)
#     return Response(serializer.data)

# ReviewDetail 에서 댓글 목록 요청
# 댓글 리스트 응답으로 반환 
@api_view(['GET'])
def comment_list(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comments = review.comments.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

# 댓글 작성 시 요청
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_create(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, review=review)
        return Response(serializer.data)

# 댓글 수정 삭제 시 요청 
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def comment_update_or_delete(request, review_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'PUT':
        if request.user == comment.user:
            serializer = CommentSerializer(comment, data=request.data) #, instance=comment
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        else:
            return Response('자기 댓글만 수정가능')
    elif request.method == 'DELETE':
        if request.user == comment.user:
            comment.delete()
            return Response('delete success', status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('자기 댓글만 삭제가능')


# 좋아요 클릭 시 요청
# 좋아요 관련 isLike, likeCounter 등 응답으로 반환 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    
    if review.like_users.filter(pk=request.user.pk).exists():
        review.like_users.remove(request.user)
        is_like = False
    else:
        review.like_users.add(request.user)
        is_like = True
    like_counter = review.like_users.count()
    
    return Response({
        'id' : review_pk,
        'userid' : request.user.pk,
        'success': True,
        'isLike': is_like,
        'likeCounter': like_counter,
    })


# Signup 이후 SetUser 에서 사용 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_user(request, movie_pk):
    
    serializer = ReviewSerializer(data=request.data)
    movie = get_object_or_404(Movie, pk=movie_pk)

    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, movie=movie) # 추후수정
        return Response('취향 분석이 성공적으로 완료되었습니다.')