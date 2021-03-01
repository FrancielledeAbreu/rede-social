
from rest_framework import serializers
from accounts.serializers import UserSerializer


class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    author = UserSerializer(read_only=True)
    comment = serializers.CharField()
    image = serializers.CharField(
        required=False, allow_blank=True, max_length=255)
    commented_on = serializers.DateTimeField(read_only=True)
