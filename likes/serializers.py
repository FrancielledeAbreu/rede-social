from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Like


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'author']

    id = serializers.IntegerField(read_only=True)
    author = UserSerializer(read_only=True)
