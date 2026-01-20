import os
from pathlib import Path

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent



# SECURITY SETTINGS


# SECURITY WARNING: keep the secret key used in production secret!
# For production: Use environment variable instead
SECRET_KEY = 'django-insecure-REPLACE-WITH-YOUR-OWN-SECRET-KEY'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']



# APPLICATION DEFINITION


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    # Two-Factor Authentication
    'django_otp',
    'django_otp.plugins.otp_totp',
    
    # Google OAuth (SSO)
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    
    # Additional packages
    'social_django',
    'django_extensions',
    
    # Local apps
    'frontend',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'myproject.urls'



# TEMPLATES


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'frontend/templates',
        ],
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

WSGI_APPLICATION = 'myproject.wsgi.application'



# DATABASE


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '?',  
        'USER': '?',  
        'PASSWORD': '?',
        'HOST': 'localhost',  
        'PORT': '3306',  
    }
}

# PASSWORD VALIDATION


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'frontend.validators.ComplexPasswordValidator',
    },
]



# AUTHENTICATION BACKENDS


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'frontend.backends.EmailBackend',
]



# AUTHENTICATION SETTINGS


LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = 'login'



# DJANGO SITES FRAMEWORK


SITE_ID = 1



# EMAIL CONFIGURATION


# Development: Emails print to console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Production: Use SMTP (configure these with environment variables)
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')



# INTERNATIONALIZATION


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True



# STATIC FILES (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'frontend/static']
STATIC_ROOT = BASE_DIR / 'staticfiles'



# MEDIA FILES (User Uploads)

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# DEFAULT PRIMARY KEY FIELD TYPE

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'