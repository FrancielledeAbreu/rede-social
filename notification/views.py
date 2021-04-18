

from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .models import Notification
from .serializers import MessageSerializer

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin,  RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin

from cache.notification_cache import NotificationCache


class NotificationView(GenericViewSet, ListModelMixin, UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Notification.objects.all()
    serializer_class = MessageSerializer

    def list(self, request, *args, **kwargs):

        notification_cache = NotificationCache(request.user)
        notifications = notification_cache.get_notification()

        if notifications:
            return Response(notifications)

        #  apenas as notificações do user logado
        queryset = Notification.objects.filter(
            user_id=request.user.id).filter(read=False)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        notification_cache.set_notification(serializer.data)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        notification_cache = NotificationCache(request.user)
        notification_cache.clear()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        notification_cache.set_notification(MessageSerializer(
            Notification.objects.all().filter(user=request.user).filter(read=False), many=True).data)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)
