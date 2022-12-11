from rest_framework import generics
# Create your views here.
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from users.models import User
from users.permissions import IsOwner, IsAnonymous
from users.serializers import UserSerializer, CreateUserSerializer


class ListUserAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    pagination_class = LimitOffsetPagination


class DetailUserAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsOwner]

    def get(self, request, *args, **kwargs):
        queryset = User.objects.get(**kwargs)
        self.check_object_permissions(request, queryset)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


class CreateUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [IsAnonymous]


class EditUserAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwner]

    def perform_destroy(self, instance):
        instance.is_valid = False
        instance.save()
        return instance
