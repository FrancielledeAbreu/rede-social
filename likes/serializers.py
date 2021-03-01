from rest_framework import serializers
from accounts.serializers import UserSerializer


class LikeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    author = UserSerializer(read_only=True)
