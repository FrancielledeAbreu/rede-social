from django.shortcuts import render
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
import ipdb


class PostView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):

        serializer = PostSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        current_user = request.user

        post = Post.objects.get_or_create(
            title=request.data['title'], description=request.data['description'], image=request.data['image'], author=current_user)[0]

        serializer = PostSerializer(post)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Comment.objects.all()
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)


class CommentIdView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request,  id: int):

        serializer = CommentSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        current_user = request.user
        post = Post.objects.get(id=id)

        comment = Comment.objects.get_or_create(
            comment=request.data['comment'], image=request.data['image'], author=current_user, post=post)[0]

        serializer = CommentSerializer(comment)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LikeIdView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request,  id: int):

        serializer = LikeSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        current_user = request.user
        post = Post.objects.get(id=id)

        like = Like.objects.get_or_create(
            author=current_user, post=post)[0]

        serializer = LikeSerializer(like)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
