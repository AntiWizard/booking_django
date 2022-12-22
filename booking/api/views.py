from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request):
    return Response({
        'swagger': reverse('swagger-ui', request=request),
        'api': reverse('api-view-list', request=request),
    })


@api_view(['GET'])
def api_views(request):
    return Response({
        'hotel': reverse('hotel-list', request=request),
        'apartment': reverse('apartment-list', request=request),
        'airplane': reverse('airplane-list', request=request),
        'bus': reverse('bus-list', request=request),
        'ship': reverse('ship-list', request=request),
    })
