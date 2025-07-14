from rest_framework import serializers
from .models import CustomUser, Profile

from djoser.serializers import UserCreateSerializer

class UserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ('id', 'email', 'username', 'password', 'role', 'date_joined')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'first_name', 'last_name', 'location', 'bio', 'phone_number']
