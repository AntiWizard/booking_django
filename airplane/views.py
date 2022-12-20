# Create your views here.
from rest_framework import generics


class ListAirplaneAPIView(generics.ListAPIView):
    pass


class RetrieveAirplaneAPIView(generics.RetrieveAPIView):
    pass


class DetailAirplaneAPIView(generics.DestroyAPIView, generics.UpdateAPIView):
    pass
