from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User
import pdb

class UsersSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(
        max_length=20,
        validators=[UniqueValidator(
            User.objects.all(), "username already taken."
        )])
    email = serializers.EmailField(
        max_length=127,
        validators=[UniqueValidator(
            User.objects.all(), "email already registered."
        )])
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    birthdate = serializers.DateField(required=False)
    is_employee = serializers.BooleanField(required=False, default=False)
    is_superuser = serializers.BooleanField(read_only=True)

    def get_is_superuser(self, obj):
        return obj.is_superuser

    def create(self, data):
        if data["is_employee"]:
            user = User.objects.create_superuser(**data)

            return user

        user = User.objects.create_user(**data)

        return user
