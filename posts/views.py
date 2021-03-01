from django.shortcuts import render
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from guardian.shortcuts import assign_perm
import ipdb


class PostView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Post.objects.all().filter(private=False)
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):

        serializer = PostSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        current_user = request.user

        post = Post.objects.get_or_create(
            **request.data,  author=current_user)[0]

        assign_perm('author', current_user, post)
        serializer = PostSerializer(post)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostPrivateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.all()

        user_following = request.user.following.all()
        # quem o user logado segue
        # pegando apenas os ids
        ids = user_following.values_list('id', flat=True)

        # pode ver os posts de quem segue, quem o author_id está na lista de ids do user logado
        private_posts = posts.filter(author_id__in=ids).filter(private=True)

        serializer_private_post = PostSerializer(private_posts, many=True)
        public_post = Post.objects.all().filter(private=False)
        serializer_public_post = PostSerializer(public_post, many=True)
        # juntando posts publicos e privados
        posts = serializer_private_post.data + serializer_public_post.data
        # organiza pelos posts em ordem cronologica
        sorted_list_posts = sorted(
            posts, key=lambda k: k['posted_on'])
        # retornar do post mais atual para o mais antigo reverter lista
        return Response(sorted_list_posts[::-1])


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
