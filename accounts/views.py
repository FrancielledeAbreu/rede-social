import re
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from .models import User
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
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


class UserView(GenericViewSet,
               RetrieveModelMixin,
               ListModelMixin,
               CreateModelMixin):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def follow(self, request, pk):

        user_to_follow = get_object_or_404(User, id=pk)

        current_user = request.user

        current_user.following.add(user_to_follow)

        return Response(f'{request.user.username} começou a seguir {user_to_follow.username}')

    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk):

        user_to_follow = get_object_or_404(User, id=pk)

        current_user = request.user

        if len(current_user.following.filter(id=pk)) > 0:

            current_user.following.remove(user_to_follow)
        else:
            return Response(f'{request.user.username} você não segue {user_to_follow.username}')

        return Response(f'{request.user.username} deixou de seguir {user_to_follow.username}')

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserNameView(GenericViewSet,
                   RetrieveModelMixin):

    def retrieve(self, request, *args, **kwargs):
        print(*args, 'fsdf')
        open_sale = get_object_or_404(User,
                                      username=kwargs['username'])

        serializer = UserSerializer(open_sale)
        return Response(serializer.data)

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = 'username'
