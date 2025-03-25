"""
Django's settings for GreenGoShop project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
from decouple import config, Csv, strtobool

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = config('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', cast=Csv())
INSTALLED_APPS = [
    'django_crontab',
    'shop.apps.ShopConfig',
    'analytics.apps.AnalyticsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
    'ckeditor_uploader',
    'imagekit',
    'django.contrib.sitemaps',
]
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ["Format", "Bold", "Italic", "Underline", "Strike", "NumberedList", "BulletedList", ],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight'],
            ["Image"],
            ['Undo', 'Redo', 'Html5video']],

        'extraPlugins': ','.join([
            'dialogui',
            'dialog',
            'button',
            'widgetselection',
            'toolbar',
            'notification',
            'clipboard',
            'lineutils',
            'widget',
            'html5video',

        ]),
    }
}
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'GreenGoShop.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'shop.context_processors.cart_renderer',
                'shop.context_processors.extras',
            ],
        },
    },
]
WSGI_APPLICATION = 'GreenGoShop.wsgi.application'

if config('DJANGO_USES_SQLITE', cast=bool):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': config('DJANGO_DATABASE_NAME'),
            'USER': config('DJANGO_DATABASE_USER'),
            'PASSWORD': config('DJANGO_DATABASE_PASSWORD'),
            'HOST': config('DJANGO_DATABASE_HOST'),
            'PORT': '',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {"level": "INFO", "handlers": ["file"]},
    "handlers": {
        "file": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": config('DJANGO_LOGGER_FILE_PATH'),
            "formatter": "app",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "WARNING",
            "propagate": True
        },
    },
    "formatters": {
        "app": {
            "format": (
                u"%(asctime)s [%(levelname)-8s] "
                "(%(module)s.%(funcName)s) %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
}

CRONJOBS = [
    ('0 2 * * *', 'shop.cron.old_carts_cleaner'),
    ('8 4 * * *', 'analytics.facebook_api.daily_spend.get_campaign_id'),
    ('0 1 * * *', 'shop.cron.reverse_offer_if_older_than_1_day')
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'CET'
USE_I18N = True
USE_TZ = True
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
