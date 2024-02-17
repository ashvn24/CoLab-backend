# import environ
from datetime import timedelta
import os
from pathlib import Path
# env = environ.Env(
#     DEBUG=(bool, False)
# )

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# environ.Env.read_env(BASE_DIR / '.env') 
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-hy%36uvhrjg_u22cc)gghd-#++o73x12!8r-g)(b+!0jv5n6t5'

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
    'corsheaders',
    'rest_framework',
    'users',
    'rest_framework_simplejwt',
    'django_celery_results',
    'django_celery_beat',
    'Admin',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "colab",
        "USER": "postgres",
        "PASSWORD": "0089ashi",
        "HOST": "localhost",
        "PORT": "5432",
    }
}


AUTH_USER_MODEL="users.User"


REST_FRAMEWORK = {
   
    'DEFAULT_AUTHENTICATION_CLASSES': (
        
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
    
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "AUTH_HEADER_TYPES": ("Bearer",),
}


CORS_ALLOW_CREDENTIALS = True

CORS_EXPOSE_HEADERS = ['Content-Type', 'X-CSRFToken']
ROOT_URLCONF = 'backend.urls'

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_HEADERS = [
    'Content-Type',
    'content-disposition',
]
CORS_ALLOWED_ORIGINS = [
  
    'http://localhost:3000',
    'http://localhost:5173',
    'http://127.0.0.1:3000'
]

CORS_ORIGIN_WHITELIST = [
    'http://google.com',
    'http://localhost:8000',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:3000'

]
SECURE_CROSS_ORIGIN_OPENER_POLICY='same-origin-allow-popups'

SECURE_REFERRER_POLICY = 'same-origin'


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
  
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#celery settings

CELERY_BROKER_URL= 'redis://127.0.0.1:6379'
CELERY_ACCEPT_CONTENT= ['application/json']
CELERY_RESULT_SERIALIZER= 'json'
CELERY_TASK_SERIALIZER=  'json' 
CELERY_TIMEZONE= 'Asia/Kolkata' #It is for time difference of server and celery

CELERY_RESULT_BACKEND = 'django-db'

#celery beat

CELERY_BEAT_SCHEDULER= 'django_celery_beat.scheduler:DatabseScheduler'

#smpt settings
EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
EMAIL_HOST_USER = 'a8e1606228d505'
EMAIL_HOST_PASSWORD = '6cbcf337a7e4f2'
EMAIL_PORT = '2525'
EMAIL_USE_TLS = True