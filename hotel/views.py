# Create your views here.
from rest_framework import generics


class ListHotelAPIView(generics.ListAPIView):
    pass


class CreateHotelAPIView(generics.CreateAPIView):
    pass


class RetrieveHotelAPIView(generics.RetrieveAPIView):
    pass


class EditHotelAPIView(generics.UpdateAPIView):
    pass


class DeleteHotelAPIView(generics.DestroyAPIView):
    pass
