from django.shortcuts import render
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from guardian.shortcuts import assign_perm
from django.core.exceptions import ObjectDoesNotExist
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


class FeedView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            queryset = Post.objects.filter(author=request.user)
            serializer = PostSerializer(queryset, many=True)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
