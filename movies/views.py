from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.response import Response

from .models import Movie, Review
from .serializers import MovieSerializer

from .review_serializers import ReviewSerializer
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404

from .user_serializers import RegisterSerializer

from rest_framework_simplejwt.tokens import RefreshToken

from django.db.models import Q

@api_view(['GET'])
def movie_list(request):
    movies = Movie.objects.all().order_by(
        '-rating',
        '-review_count'
    )

    serializer = MovieSerializer(movies, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def movie_detail(request, pk):
    movie = get_object_or_404(Movie, id=pk)

    serializer = MovieSerializer(movie)

    data = serializer.data

    data['review_count'] = (
        movie.reviews.count()
    )

    return Response(data)


@api_view(['POST'])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'User registered successfully',

            'refresh': str(refresh),

            'access': str(refresh.access_token),
        })

    return Response(serializer.errors)


@api_view(['GET'])
def movie_reviews(request, movie_id):
    reviews = Review.objects.filter(
        movie_id=movie_id
    ).order_by('-created_at')

    serializer = ReviewSerializer(
        reviews,
        many=True
    )

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review(request, movie_id):
    movie = Movie.objects.get(id=movie_id)

    review = Review.objects.filter(
        user=request.user,
        movie=movie
    ).first()

    if review:
        review.rating = request.data['rating']

        review.review_text = request.data['review_text']

        review.save()

        message = 'Review updated successfully'

    else:
        Review.objects.create(
            user=request.user,
            movie=movie,
            rating=request.data['rating'],
            review_text=request.data['review_text']
        )

        message = 'Review added successfully'

    reviews = Review.objects.filter(
        movie=movie
    )

    average_rating = (
        sum(review.rating for review in reviews)
        / reviews.count()
    )

    movie.rating = round(average_rating, 1)
    movie.review_count = reviews.count()

    movie.save()

    return Response({
        'message': message
    })

@api_view(['GET'])
def search_movies(request):
    query = request.GET.get('q')

    movies = Movie.objects.filter(
        Q(title__icontains=query) |
        Q(genre__icontains=query) |
        Q(language__icontains=query)
    )

    serializer = MovieSerializer(
        movies,
        many=True
    )

    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user

    reviews = Review.objects.filter(
        user=user
    )

    return Response({
        'username': user.username,

        'email': user.email,

        'review_count': reviews.count(),

        'reviews': ReviewSerializer(
            reviews,
            many=True
        ).data
    })

@api_view(['GET'])
def related_movies(request, movie_id):
    movie = Movie.objects.get(id=movie_id)

    related = Movie.objects.filter(
        genre=movie.genre
    ).exclude(
        id=movie.id
    ).order_by(
        '-rating',
        '-review_count'
    )[:4]

    serializer = MovieSerializer(
        related,
        many=True
    )

    return Response(serializer.data)


@api_view(['GET'])
def top_rated_movies(request):
    movies = Movie.objects.all().order_by(
        '-rating'
    )[:10]

    serializer = MovieSerializer(
        movies,
        many=True
    )

    return Response(serializer.data)


@api_view(['GET'])
def most_reviewed_movies(request):
    movies = Movie.objects.all().order_by(
        '-review_count'
    )[:10]

    serializer = MovieSerializer(
        movies,
        many=True
    )

    return Response(serializer.data)


@api_view(['GET'])
def latest_movies(request):
    movies = Movie.objects.all().order_by(
        '-release_date'
    )[:10]

    serializer = MovieSerializer(
        movies,
        many=True
    )

    return Response(serializer.data)

@api_view(['GET'])
def featured_movies(request):
    movies = Movie.objects.all().order_by(
        '-rating',
        '-review_count'
    )[:5]

    serializer = MovieSerializer(
        movies,
        many=True
    )

    return Response(serializer.data)