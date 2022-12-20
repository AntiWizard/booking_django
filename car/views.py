# Create your views here.
from rest_framework import generics


class ListCarAPIView(generics.ListAPIView):
    pass


class CreateCarAPIView(generics.CreateAPIView):
    pass


class RetrieveCarAPIView(generics.RetrieveAPIView):
    pass


class EditCarAPIView(generics.UpdateAPIView):
    pass


class DeleteCarAPIView(generics.DestroyAPIView):
    pass
