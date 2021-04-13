
from rest_framework import status
from rest_framework.response import Response

from .models import Comment
from posts.models import Post
from .serializers import CommentSerializer
from notification.models import Notification

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, DestroyModelMixin

from django.shortcuts import get_object_or_404
from rest_framework.decorators import action


class CommentView(GenericViewSet,
                  ListModelMixin, DestroyModelMixin):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    @action(detail=True, methods=['post'])
    def new(self, request, pk):

        serializer = CommentSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        current_user = request.user
        post = get_object_or_404(Post, id=pk)

        comment = Comment.objects.get_or_create(
            **request.data, author=current_user, post=post)[0]

        notification = Notification.objects.create(user=post.author, author_id=current_user.id,
                                                   message_type="Comentario", text=f'Você recebeu um comentário de {current_user.username} no Post {post.title}')

        serializer = CommentSerializer(comment)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if not instance.author.id == request.user.id:
            return Response({'errors': 'you are not author of this comment'}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
