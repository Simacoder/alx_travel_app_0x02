from rest_framework import serializers
from .models import Booking, Listing, Review, Payment  


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Review
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    booking = BookingSerializer(read_only=True)  # Nested booking info
    booking_id = serializers.UUIDField(write_only=True)  # Accept booking_id on creation

    class Meta:
        model = Payment
        fields = [
            'payment_id',
            'booking',
            'booking_id',
            'amount',
            'status',
            'transaction_reference',
            'chapa_transaction_id',
            'created_at'
        ]
        read_only_fields = ['payment_id', 'status', 'transaction_reference', 'chapa_transaction_id', 'created_at']
