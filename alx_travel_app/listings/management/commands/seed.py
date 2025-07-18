from django.core.management.base import BaseCommand
from listings.models import Listing
from django.contrib.auth.models import User
import random

class Command(BaseCommand):
    help = 'Seed the database with sample listings'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Seeding data..."))

        # Create sample listings
        for i in range(10):
            Listing.objects.create(
                title=f"Sample Listing {i}",
                description="This is a sample listing for testing.",
                price_per_night=random.randint(50, 300),
                location="Nairobi",
            )

        self.stdout.write(self.style.SUCCESS("Seeding completed."))
