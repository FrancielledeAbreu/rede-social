from django.shortcuts import render
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Comment
from posts.models import Post
from .serializers import CommentSerializer
from notification.models import Notification
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


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
            **request.data, author=current_user, post=post)[0]

        notification = Notification.objects.create(user=post.author, author_id=current_user.id,
                                                   message_type="Comentario", text=f'Você recebeu um comentário de {current_user.username} no Post {post.title}')

        serializer = CommentSerializer(comment)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
