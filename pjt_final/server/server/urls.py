from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('movies/', include('movies.urls')),
    path('reviews/', include('reviews.urls')),
    # dj-rest-auth
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/profile/', include('accounts.urls')),
    path('accounts/signup/', include('dj_rest_auth.registration.urls')),
]
