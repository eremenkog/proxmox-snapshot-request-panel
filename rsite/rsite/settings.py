from pathlib import Path
from .secrets import SQL_DB_NAME, SQL_USER, SQL_PASSWORD, SQL_HOST, SQL_PORT
from .secrets import AUTH_LDAP_SERVER_URI, AUTH_LDAP_BIND_DN, AUTH_LDAP_BIND_PASSWORD
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType
import os, ldap

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-$q*e0w!@+fwkw1841zzn(xen8^vj(_*9=%c(l&n1zyt3kso1u_'

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
    'rapp',
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

ROOT_URLCONF = 'rsite.urls'

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

WSGI_APPLICATION = 'rsite.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': SQL_DB_NAME,
        'USER': SQL_USER,
        'PASSWORD': SQL_PASSWORD,
        'HOST': SQL_HOST,
        'PORT': SQL_PORT,
    }
}


# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'rapp', 'static'),
]

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# LDAP auth block


AUTHENTICATION_BACKENDS = [
  'django_auth_ldap.backend.LDAPBackend',
  'django.contrib.auth.backends.ModelBackend',
]
# LDAP Server Settings
AUTH_LDAP_SERVER_URI = AUTH_LDAP_SERVER_URI
AUTH_LDAP_BIND_DN = AUTH_LDAP_BIND_DN
AUTH_LDAP_BIND_PASSWORD = AUTH_LDAP_BIND_PASSWORD
# Map LDAP attributes to Django user fields
AUTH_LDAP_USER_ATTR_MAP = {
  "username":   "sAMAccountName",
  "first_name": "givenName",
  "last_name":  "sn",
  "email":      "mail",
}

AUTH_LDAP_USER_SEARCH = LDAPSearch(
  "OU=Lab_Users,DC=lab,DC=domain",  # LDAP search base
  ldap.SCOPE_SUBTREE,               # Scope
  "(sAMAccountName=%(user)s)",      # LDAP search filter
)

#import logging
#logger = logging.getLogger('django_auth_ldap')
#logger.addHandler(logging.StreamHandler())  # Print logs to the console
#logger.setLevel(logging.DEBUG)  # Set the logging level to DEBUG