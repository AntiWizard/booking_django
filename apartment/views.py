from rest_framework import generics


class ListApartmentAPIView(generics.ListAPIView):
    pass


class CreateApartmentAPIView(generics.CreateAPIView):
    pass


class RetrieveApartmentAPIView(generics.RetrieveAPIView):
    pass


class EditApartmentAPIView(generics.UpdateAPIView):
    pass


class DeleteApartmentAPIView(generics.DestroyAPIView):
    pass
