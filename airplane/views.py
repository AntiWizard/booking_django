from rest_framework import generics


class ListAirplaneAPIView(generics.ListAPIView):
    pass


class CreateAirplaneAPIView(generics.CreateAPIView):
    pass


class RetrieveAirplaneAPIView(generics.RetrieveAPIView):
    pass


class EditAirplaneAPIView(generics.UpdateAPIView):
    pass


class DeleteAirplaneAPIView(generics.DestroyAPIView):
    pass
