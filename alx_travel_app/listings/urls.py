# listings/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, BookingViewSet, ReviewViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'listings', ListingViewSet, basename='listing')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'reviews', ReviewViewSet, basename='review')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('api/', include(router.urls)),
]

#  Add API root view for better API browsability
# This will show all available endpoints at /api/
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(['GET'])
def api_root(request, format=None):
    """API root endpoint that lists all available endpoints."""
    return Response({
        'listings': reverse('listing-list', request=request, format=format),
        'bookings': reverse('booking-list', request=request, format=format),
        'reviews': reverse('review-list', request=request, format=format),
    })

# Include the api_root in urlpatterns if you want a custom root
# urlpatterns += [
#     path('api/', api_root),
# ]