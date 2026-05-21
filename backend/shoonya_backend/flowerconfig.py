import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shoonya_backend.settings")
django.setup()

from django.conf import settings

address = settings.FLOWER_ADDRESS
port = settings.FLOWER_PORT
broker_url = settings.CELERY_BROKER_URL
broker = settings.CELERY_BROKER_URL

# Enable basic authentication
flower_username = settings.FLOWER_USERNAME
flower_password = settings.FLOWER_PASSWORD
basic_auth = f"{flower_username}:{flower_password}"
