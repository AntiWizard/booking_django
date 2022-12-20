# Create your views here.
from rest_framework import generics


class ListShipAPIView(generics.ListAPIView):
    pass


class CreateShipAPIView(generics.CreateAPIView):
    pass


class RetrieveShipAPIView(generics.RetrieveAPIView):
    pass


class EditShipAPIView(generics.UpdateAPIView):
    pass


class DeleteShipAPIView(generics.DestroyAPIView):
    pass
