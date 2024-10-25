# fitverseBackEnd/settings/prod.py

from .base import *

# Production-specific settings
DEBUG = False

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',')

# Configure your production database settings here
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.postgresql',  # For example, if using PostgreSQL
    'NAME': os.environ.get('DB_NAME'),
    'USER': os.environ.get('DB_USER'),
    'PASSWORD': os.environ.get('DB_PASSWORD'),
    'HOST': os.environ.get('DB_HOST'),
    'PORT': os.environ.get('DB_PORT'),
}

# Static and media files configuration for production
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
