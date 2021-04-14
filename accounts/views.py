
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin

from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


from .serializers import UserSerializer
from .models import User


from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework.decorators import action


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
               CreateModelMixin,
               UpdateModelMixin,
               DestroyModelMixin):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

# somente o user logado pode editar e deletar sua conta

    def update(self, request, *args, **kwargs):

        if int(kwargs['pk']) == request.user.id:

            partial = kwargs.pop('partial', False)

            instance = self.get_object()

            serializer = self.get_serializer(
                instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)

        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):

        if int(kwargs['pk']) == request.user.id:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

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

        open_sale = get_object_or_404(User,
                                      username=kwargs['username'])

        serializer = UserSerializer(open_sale)
        return Response(serializer.data)

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = 'username'
