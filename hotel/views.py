# Create your views here.
from rest_framework import generics


class ListHotelAPIView(generics.ListAPIView):
    pass


class CreateHotelAPIView(generics.CreateAPIView):
    pass


class DetailHotelAPIView(generics.UpdateAPIView, generics.DestroyAPIView):
    pass


class RetrieveHotelAPIView(generics.RetrieveAPIView):
    pass
