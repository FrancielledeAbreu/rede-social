
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Notification
from .serializers import MessageSerializer
from django.core.exceptions import ObjectDoesNotExist
import ipdb


class NotificationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            queryset = Notification.objects.filter(user_id=request.user.id)
            serializer = MessageSerializer(queryset, many=True)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
