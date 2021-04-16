
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from .models import Post
from .serializers import PostSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from guardian.shortcuts import assign_perm

import ipdb

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin

from cache.timeline import TimelineCache


class PostView(GenericViewSet, ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):

        timeline_cache = TimelineCache()
        timeline = timeline_cache.get_timeline()

        if timeline:
            return Response(timeline)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        timeline_cache.set_timeline(serializer.data)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        current_user = request.user

        timeline_cache = TimelineCache()
        timeline_cache.clear()

        post = Post.objects.get_or_create(
            **request.data,  author=current_user)[0]

        serializer = PostSerializer(post)

        assign_perm('author', current_user, post)

        timeline_cache.set_timeline(
            PostSerializer(Post.objects.all(), many=True).data)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):

        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if not request.user.has_perm('posts.author', instance):
            return Response({'errors': 'you are not author of this post'}, status=status.HTTP_403_FORBIDDEN)

        timeline_cache = TimelineCache()
        timeline_cache.clear()

        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        timeline_cache.set_timeline(
            PostSerializer(Post.objects.all(), many=True).data)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if not request.user.has_perm('posts.author', instance):
            return Response({'errors': 'you are not author of this post'}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)

        timeline_cache = TimelineCache()
        timeline_cache.clear()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
