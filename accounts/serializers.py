from rest_framework import serializers
from rest_framework import serializers
from .models import User

# class UserSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     username = serializers.CharField()
#     password = serializers.CharField(write_only=True)
#     type = serializers.CharField(read_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'type']
