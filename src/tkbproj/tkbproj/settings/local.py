import os

from .base import *  # noqa

DATABASES = {
    "default": {
        "ENGINE": os.environ["DB_ENGINE"],
        "NAME": os.environ["DB_DB"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": os.environ["DB_HOST"],
        "PORT": os.environ["DB_PORT"],
    }
}

CELERY_BROKER_URL = os.environ["CELERY_BROKER_URL"]
CELERY_RESULT_BACKEND = os.environ["CELERY_RESULT_BACKEND"]

MEDIA_URL = "http://127.0.0.1:8001/media/"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

USE_X_FORWARDED_HOST = True
