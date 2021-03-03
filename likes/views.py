from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Like
from .serializers import LikeSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from posts.models import Post
from notification.models import Notification
from posts.serializers import PostSerializer
from django.core.exceptions import ObjectDoesNotExist
import ipdb


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

        notification = Notification.objects.create(user=post.author, author_id=current_user.id,
                                                   message_type="Like", text=f'Você recebeu um like de {current_user.username} no Post {post.title}')
        serializer = LikeSerializer(like)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request,  id: int):
        post = Post.objects.get(id=id)

        if not request.user.has_perm('posts.author', post):
            return Response({'errors': 'you are not author of this post'}, status=status.HTTP_403_FORBIDDEN)

        if request.data.get('title'):
            post.title = request.data['title']

        if request.data.get('description'):
            post.description = request.data['description']

        if request.data.get('image'):
            post.image = request.data['image']

        if request.data.get('private'):
            post.private = request.data['private']

        post.save()
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id: int):

        try:
            post = Post.objects.get(id=id)
            if not request.user.has_perm('posts.author', post):
                return Response({'errors': 'you are not author of this post'}, status=status.HTTP_403_FORBIDDEN)

        except ObjectDoesNotExist:
            return Response({'message': 'post does not exist'}, status=status.HTTP_404_NOT_FOUND)

        post.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
