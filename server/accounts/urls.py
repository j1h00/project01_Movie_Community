from . import views
from django.urls import path

app_name = 'accounts'

urlpatterns = [
    # path('', views.signup, name="signup"),
    path('myprofile/', views.myprofile, name="myprofile"),
    path('<int:user_pk>/', views.user_profile, name="userprofile"),
]