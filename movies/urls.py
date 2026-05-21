from django.urls import path
from .views import movie_list, movie_detail, register_user, search_movies, user_profile, related_movies, featured_movies
from .views import (
    movie_reviews,
    add_review,
    top_rated_movies,
    most_reviewed_movies,
    latest_movies,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('movies/', movie_list),

    path('movies/<int:pk>/', movie_detail),

    path('register/', register_user),

    path('login/', TokenObtainPairView.as_view()),

    path('token/refresh/', TokenRefreshView.as_view()),

    path(
        'movies/<int:movie_id>/reviews/',
        movie_reviews
    ),

    path(
        'movies/<int:movie_id>/add-review/',
        add_review
    ),

    path('search/', search_movies),

    path('profile/', user_profile),

    path(
        'movies/<int:movie_id>/related/',
        related_movies
    ),

    path(
        'top-rated/',
        top_rated_movies
    ),

    path(
        'most-reviewed/',
        most_reviewed_movies
    ),

    path(
        'latest/',
        latest_movies
    ),

    path(
        'featured/',
        featured_movies
    ),
]