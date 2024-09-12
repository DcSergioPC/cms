"""
Django settings for cms project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY',default='django-insecure-!rm=g3wijsq8($0o5k6^82byrg+yc=5zd_gst4eq4-f+bu2%r!')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG',default=True)

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS',default="*").split(",")
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    "whitenoise.runserver_nostatic",
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'allauth.usersessions',
    'cms', #agregado
    'cuentas.apps.CuentasConfig', #agregado
    'articulos.apps.ArticulosConfig',  #agregado
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.openid_connect',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",  # new
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'cms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cms.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('POSTGRES_ENGINE',default='django.db.backends.sqlite3'),
        'NAME': os.environ.get('POSTGRES_NAME',default=BASE_DIR / 'db.sqlite3'),
        "USER": os.environ.get('POSTGRES_USER',default=''),
        "PASSWORD": os.environ.get('POSTGRES_PASSWORD',default=''),
        "HOST": os.environ.get('POSTGRES_HOST',default=''),
        "PORT": os.environ.get('POSTGRES_PORT',default="5432"),
        'OPTIONS': {
            'sslmode': os.environ.get('POSTGRES_SSLMODE', default='disable'),  # Agrega el modo SSL aquí
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATICFILES_DIRS = [BASE_DIR / 'static']

STATIC_URL = 'static/'

########################################
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
########################################3

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#documentacion
LOGIN_URL = '/cuentas/login'
LOGIN_REDIRECT_URL = '/articulos'
LOGOUT_REDIRECT_URL = f'{os.getenv("KEYCLOAK_SERVER_HOST")}/realms/{os.getenv("KEYCLOAK_REALM")}/protocol/openid-connect/logout?post_logout_redirect_uri={os.getenv("DJANGO_SERVER_HOST")}/cuentas/login&client_id={os.getenv("KEYCLOAK_CLIENT_ID")}'


AUTH_USER_MODEL = 'cuentas.CustomUser'
SOCIALACCOUNT_LOGIN_ON_GET=True

AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend'
]
DJANGO_SERVER_HOST=os.getenv('DJANGO_SERVER_HOST')
KEYCLOAK_CLIENT_ID = os.getenv('KEYCLOAK_CLIENT_ID')
SOCIALACCOUNT_PROVIDERS = {
    "openid_connect": {
        "APPS": [
            {
                "provider_id": "keycloak",
                "name": "Keycloak",
                "client_id": KEYCLOAK_CLIENT_ID,
                "secret": os.getenv('KEYCLOAK_SECRET'),
                "settings": {
                    "server_url": f'{os.getenv("KEYCLOAK_SERVER_HOST")}/realms/{os.getenv("KEYCLOAK_REALM")}/.well-known/openid-configuration',
                },
            }
        ]
    }
}
SITE_ID=1
SITE_NAME=os.getenv('SITE_NAME', 'localhost')

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"  # new

CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', 'localhost').split(",")

ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_EMAIL_REQUIRED = False