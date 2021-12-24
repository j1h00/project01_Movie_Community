from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.movie_list),
    path('<int:movie_pk>/', views.movie_detail),
    path('search/', views.movie_search),
    # path('<int:movie_pk>/likes', views.add_playlist),
]