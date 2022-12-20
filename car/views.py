# Create your views here.
from rest_framework import generics


class ListCarAPIView(generics.ListAPIView):
    pass


class RetrieveCarAPIView(generics.RetrieveAPIView):
    pass


class DetailCarAPIView(generics.DestroyAPIView, generics.UpdateAPIView):
    pass
