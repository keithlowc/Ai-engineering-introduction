"""Django settings module with environment-based configuration."""

import os
from pathlib import Path

from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings - loaded from environment variables
SECRET_KEY = config("SECRET_KEY", default=None)
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable must be set")

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="localhost,127.0.0.1",
    cast=lambda v: [s.strip() for s in v.split(",")],
)

# Database configuration - loaded from environment variables
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME", default="myapp"),
        "USER": config("DB_USER", default="dbuser"),
        "PASSWORD": config("DB_PASSWORD", default=None),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", default="5432"),
    }
}

# Redis configuration - loaded from environment variables
REDIS_URL = (
    f"redis://:{config('REDIS_PASSWORD', default=None)}@"
    f"{config('REDIS_HOST', default='localhost')}:"
    f"{config('REDIS_PORT', default='6379')}"
)

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
]

MIDDLEWARE = []

ROOT_URLCONF = "config.urls"

TEMPLATES = []

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True
