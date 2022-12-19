# Create your views here.
from rest_framework import generics


class ListShipAPIView(generics.ListAPIView):
    pass


class RetrieveShipAPIView(generics.RetrieveAPIView):
    pass


class DetailShipAPIView(generics.DestroyAPIView, generics.UpdateAPIView):
    pass
