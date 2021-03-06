from django.db.models.deletion import SET_NULL
from rest_framework import serializers
from accounts.serializers import UserSerializer
from comments.serializers import CommentSerializer
from likes.serializers import LikeSerializer
from .models import Post


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'description',
                  'image', 'posted_on', 'private', 'comment', 'like']

    id = serializers.IntegerField(read_only=True)
    author = UserSerializer(read_only=True)
    title = serializers.CharField()
    description = serializers.CharField()
    image = serializers.CharField(
        required=False, allow_blank=True, max_length=255)
    posted_on = serializers.DateTimeField(read_only=True)
    private = serializers.BooleanField(default=False)
    comment = CommentSerializer(many=True, read_only=True)
    like = LikeSerializer(many=True, read_only=True)
