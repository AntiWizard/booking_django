from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_views(request, _format=None):
    return Response({
        'hotel': reverse('hotel-list', request=request, format=_format),
        'apartment': reverse('apartment-list', request=request, format=_format),
        'airplane': reverse('airplane-list', request=request, format=_format),
        'car': reverse('car-list', request=request, format=_format),
        'ship': reverse('ship-list', request=request, format=_format),
    })
