import os
from celery import Celery

# Set default Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_travel_app.settings")

app = Celery("alx_travel_app")

# Read config from Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks in installed apps
app.autodiscover_tasks()
