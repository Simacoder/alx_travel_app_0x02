# listings/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from .models import Listing, Booking, Review
from .serializers import ListingSerializer, BookingSerializer, ReviewSerializer

User = get_user_model()


class ListingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Listing objects.
    Provides CRUD operations for listings.
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'listing_id'

    def perform_create(self, serializer):
        """Set the host to the current user when creating a listing."""
        serializer.save(host=self.request.user)

    def get_permissions(self):
        """
        Instantiate and return the list of permissions that this view requires.
        Only the host can update or delete their own listings.
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        """
        Optionally restricts the returned listings to those owned by the user,
        by filtering against a `host` query parameter in the URL.
        """
        queryset = Listing.objects.all()
        host = self.request.query_params.get('host', None)
        if host is not None:
            queryset = queryset.filter(host__username=host)
        return queryset

    def update(self, request, *args, **kwargs):
        """Only allow hosts to update their own listings."""
        listing = self.get_object()
        if listing.host != request.user:
            return Response(
                {"detail": "You can only update your own listings."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Only allow hosts to delete their own listings."""
        listing = self.get_object()
        if listing.host != request.user:
            return Response(
                {"detail": "You can only delete your own listings."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Booking objects.
    Users can only see and manage their own bookings.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'booking_id'

    def get_queryset(self):
        """Users can only see their own bookings."""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Set the user to the current user when creating a booking."""
        listing_id = self.request.data.get('listing')
        try:
            listing = Listing.objects.get(listing_id=listing_id)
            serializer.save(user=self.request.user, listing=listing)
        except Listing.DoesNotExist:
            return Response(
                {"detail": "Listing not found."},
                status=status.HTTP_404_NOT_FOUND
            )

    def create(self, request, *args, **kwargs):
        """Override create to handle listing lookup properly."""
        listing_id = request.data.get('listing')
        if not listing_id:
            return Response(
                {"detail": "Listing ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            listing = Listing.objects.get(listing_id=listing_id)
        except Listing.DoesNotExist:
            return Response(
                {"detail": "Listing not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if user is trying to book their own listing
        if listing.host == request.user:
            return Response(
                {"detail": "You cannot book your own listing."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, listing=listing)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """Only allow users to update their own bookings."""
        booking = self.get_object()
        if booking.user != request.user:
            return Response(
                {"detail": "You can only update your own bookings."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Only allow users to delete their own bookings."""
        booking = self.get_object()
        if booking.user != request.user:
            return Response(
                {"detail": "You can only delete your own bookings."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Review objects.
    Provides CRUD operations for reviews with proper filtering.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'review_id'

    def get_queryset(self):
        """
        Filter reviews by listing if listing_id is provided in query params.
        """
        queryset = Review.objects.all()
        listing_id = self.request.query_params.get('listing_id', None)
        if listing_id is not None:
            queryset = queryset.filter(listing__listing_id=listing_id)
        return queryset

    def perform_create(self, serializer):
        """Set the user to the current user when creating a review."""
        listing_id = self.request.data.get('listing')
        try:
            listing = Listing.objects.get(listing_id=listing_id)
            serializer.save(user=self.request.user, listing=listing)
        except Listing.DoesNotExist:
            return Response(
                {"detail": "Listing not found."},
                status=status.HTTP_404_NOT_FOUND
            )

    def create(self, request, *args, **kwargs):
        """Override create to handle listing lookup and validation."""
        listing_id = request.data.get('listing')
        if not listing_id:
            return Response(
                {"detail": "Listing ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            listing = Listing.objects.get(listing_id=listing_id)
        except Listing.DoesNotExist:
            return Response(
                {"detail": "Listing not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if user already reviewed this listing
        if Review.objects.filter(user=request.user, listing=listing).exists():
            return Response(
                {"detail": "You have already reviewed this listing."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, listing=listing)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """Only allow users to update their own reviews."""
        review = self.get_object()
        if review.user != request.user:
            return Response(
                {"detail": "You can only update your own reviews."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Only allow users to delete their own reviews."""
        review = self.get_object()
        if review.user != request.user:
            return Response(
                {"detail": "You can only delete your own reviews."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def my_reviews(self, request):
        """Get all reviews by the current user."""
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        reviews = Review.objects.filter(user=request.user)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)