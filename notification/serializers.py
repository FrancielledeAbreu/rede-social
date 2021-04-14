from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Notification


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ['id', 'user', 'author_id',
                  'message_type', 'created_at', 'text', 'read']

    id = serializers.IntegerField(read_only=True)
    user = UserSerializer()
    author_id = serializers.IntegerField()
    message_type = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    text = serializers.CharField()
    read = serializers.BooleanField(default=False)
