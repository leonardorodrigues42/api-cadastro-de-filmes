from rest_framework import serializers
from users.serializer import UsersSerializer
from .models import Movie, Rating, MovieOrder
from django.shortcuts import get_object_or_404
import pdb

class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(max_length=10, required=False)
    rating = serializers.ChoiceField(choices=Rating.choices, required=False)
    synopsis = serializers.CharField(max_length=None, required=False)
    added_by = serializers.SerializerMethodField()

    def get_added_by(self, obj):
        return obj.user.email

    def create(self, data):
        movie = Movie.objects.create(**data)        
        return movie


class MovieOrderSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.SerializerMethodField()
    buyed_at = serializers.ReadOnlyField()
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    buyed_by = serializers.SerializerMethodField()
    
    def get_title(self, obj):
        return obj.movie.title
    
    def get_buyed_by(self, obj):
        return obj.user.email

    
    def create(self, validated_data):
        return MovieOrder.objects.create(**validated_data)
