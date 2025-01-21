import os, ldap
from pathlib import Path
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType
from .secrets import AUTH_LDAP_SERVER_URI, AUTH_LDAP_BIND_DN, AUTH_LDAP_BIND_PASSWORD, AUTH_LDAP_SCOPE
from .secrets import DJANGO_SECRET_KEY

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = DJANGO_SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'request_snapshot_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'request_snapshot.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'request_snapshot.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'request_snapshot_app', 'static'),
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# LDAP Authentication

AUTHENTICATION_BACKENDS = [
  'django_auth_ldap.backend.LDAPBackend',
  'django.contrib.auth.backends.ModelBackend',
]

## LDAP Server Settings
AUTH_LDAP_SERVER_URI = AUTH_LDAP_SERVER_URI
AUTH_LDAP_BIND_DN = AUTH_LDAP_BIND_DN
AUTH_LDAP_BIND_PASSWORD = AUTH_LDAP_BIND_PASSWORD

### Map LDAP attributes to Django user fields
AUTH_LDAP_USER_ATTR_MAP = {
  "username":   "sAMAccountName",
  "first_name": "givenName",
  "last_name":  "sn",
  "email":      "mail",
}

AUTH_LDAP_USER_SEARCH = LDAPSearch(
  AUTH_LDAP_SCOPE,  # LDAP search base
  ldap.SCOPE_SUBTREE,               # Scope
  "(sAMAccountName=%(user)s)",      # LDAP search filter
)

#### Debug
#import logging
#logger = logging.getLogger('django_auth_ldap')

# Print logs to the console
#logger.addHandler(logging.StreamHandler())

# Set the logging level to DEBUG
#logger.setLevel(logging.DEBUG)