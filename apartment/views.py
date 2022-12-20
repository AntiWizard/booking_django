from rest_framework import generics


class ListApartmentAPIView(generics.ListAPIView):
    pass


class CreateApartmentAPIView(generics.CreateAPIView):
    pass


class DetailApartmentAPIView(generics.UpdateAPIView, generics.DestroyAPIView):
    pass


class RetrieveApartmentAPIView(generics.RetrieveAPIView):
    pass
