
from rest_framework import status
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from posts.models import Post
from .models import Like
from .serializers import LikeSerializer
from notification.models import Notification
from posts.serializers import PostSerializer
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin


class LikeIdView(GenericViewSet, CreateModelMixin):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    @action(detail=True, methods=['post'])
    def like(self, request, *args, **kwargs):

        current_user = request.user
        post = Post.objects.get(id=int(kwargs['pk']))

        like = Like.objects.get_or_create(
            author=current_user, post=post)[0]

        notification = Notification.objects.create(user=post.author, author_id=current_user.id,
                                                   message_type="Like", text=f'Você recebeu um like de {current_user.username} no Post {post.title}')
        serializer = LikeSerializer(like)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
