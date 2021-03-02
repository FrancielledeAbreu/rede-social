import re
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from rest_framework import status
from .models import User
import ipdb


class AccountView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(**request.data)
        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(
            username=request.data["username"], password=request.data["password"])

        if user is not None:
            token = Token.objects.get_or_create(user=user)[0]
            return Response({'token': token.key})

        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class UserView(APIView):
    def get(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


class UserIdView(APIView):
    def get(self, request,  id: int):
        queryset = User.objects.get(id=id)
        serializer = UserSerializer(queryset)

        return Response(serializer.data)

    def post(self, request,  id: int):

        user_to_follow = User.objects.get(id=id)

        current_user = request.user
        # ipdb.set_trace()
        current_user.following.add(user_to_follow)
        return Response("ok")
