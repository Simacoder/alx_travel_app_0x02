# listings/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, BookingViewSet, ReviewViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'listings', ListingViewSet, basename='listing')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'reviews', ReviewViewSet, basename='review')

# API root endpoint that lists all available endpoints
@api_view(['GET'])
def api_root(request, format=None):
    """Custom API root view for better browsability."""
    return Response({
        'listings': reverse('listing-list', request=request, format=format),
        'bookings': reverse('booking-list', request=request, format=format),
        'reviews': reverse('review-list', request=request, format=format),
    })

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', api_root, name='api-root'),  # override DRF default root
]
