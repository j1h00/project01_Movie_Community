from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('create/<int:movie_pk>/', views.review_create),
    path('setuser/<int:movie_pk>/', views.set_user),

    path('myreview/<int:movie_pk>/', views.my_review_by_movie),
    path('bymovie/<int:movie_pk>/', views.review_list_by_movie),

    path('detail/<int:review_pk>/', views.review_detail),
    path('<int:review_pk>/', views.review_update_or_delete),

    
    path('<int:review_pk>/comments/', views.comment_list),
    path('<int:review_pk>/comments/create/', views.comment_create),
    path('<int:review_pk>/comments/<int:comment_pk>/', views.comment_update_or_delete),
    path('<int:review_pk>/likes/', views.like, name='like'),

    # path('byuser/<int:user_pk>/', views.review_list_by_user),
    # path('byuser/<int:user_pk>/comments/', views.comment_list_by_user),
    # path('', views.review_list_all),
]
