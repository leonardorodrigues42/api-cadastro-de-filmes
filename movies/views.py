from .serializers import MovieSerializer, MovieOrderSerializer
from .permissions import CustomPermissionMovie
from django.shortcuts import get_object_or_404
from .models import Movie

from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTAuthentication

import pdb

class MovieView(APIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomPermissionMovie]


    def get(self, request):
        movies = Movie.objects.all()
        page_size=2
        result_page = self.paginate_queryset(movies, request)
        
        serializer = MovieSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)


    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response(serializer.data, status.HTTP_201_CREATED)


class MovieDatailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomPermissionMovie]


    def get(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        movie = MovieSerializer(movie)
        
        return Response(movie.data)


    def delete(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        if movie:
            movie.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class MovieOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        serializer = MovieOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, movie=movie)
        
        return Response(serializer.data, status.HTTP_201_CREATED)
    