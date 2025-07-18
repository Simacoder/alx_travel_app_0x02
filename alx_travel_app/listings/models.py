from django.db import models
from django.contrib.auth.models import User
import uuid
from django.core.validators import MinValueValidator,MaxValueValidator


class Listing(models.Model):
    listing_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(null=False)
    location = models.CharField(max_length=100, null=False)
    price_per_night = models.DecimalField(decimal_places=2,max_digits=9,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Booking(models.Model):
    BOOKING_STATUS = {
        "pending": "PENDING",
        "confirmed": "CONFIRMED",
        "cancelled": "CANCELLED",
    }

    booking_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(decimal_places=2,max_digits=9,null=False)
    status = models.CharField(choices=BOOKING_STATUS,max_length=15, null=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    review_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)],null=False)
    comment = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)