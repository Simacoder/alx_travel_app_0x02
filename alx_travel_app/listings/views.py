# alx_travel_app_0x00/alx_travel_app/listings/views.py

# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Listing, Booking, Review
from .serializers import ListingSerializer, BookingSerializer, ReviewSerializer
from django.contrib.auth import get_user_model
User = get_user_model()

# Listing Views
class ListingListCreateView(generics.ListCreateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)

class ListingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'listing_id'

# Booking Views
class BookingListCreateView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can only see their own bookings
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        listing_id = self.request.data.get('listing')
        listing = Listing.objects.get(listing_id=listing_id)
        serializer.save(user=self.request.user, listing=listing)

class BookingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'booking_id'

    def get_queryset(self):
        # Users can only access their own bookings
        return self.queryset.filter(user=self.request.user)

# Review Views
class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Filter reviews by listing if listing_id is provided
        listing_id = self.request.query_params.get('listing_id')
        if listing_id:
            return self.queryset.filter(listing__listing_id=listing_id)
        return self.queryset

    def perform_create(self, serializer):
        listing_id = self.request.data.get('listing')
        listing = Listing.objects.get(listing_id=listing_id)
        serializer.save(user=self.request.user, listing=listing)

class ReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'review_id'