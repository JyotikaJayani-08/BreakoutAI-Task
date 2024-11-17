"""
Django settings for email_app project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv  # For loading environment variables from a .env file

# Load environment variables from .env
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = True
ALLOWED_HOSTS = []

# OAuth Google Client and Project ID (for Google Sheets API)
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
OAUTH_REDIRECT_URI = os.getenv("OAUTH_REDIRECT_URI")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dashboard',  # Our custom app
    'background_task',  # For handling background email tasks
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

ROOT_URLCONF = 'email_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # Directory for template files
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

WSGI_APPLICATION = 'email_app.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# .env setup for sensitive data
# Please set the following in .env:
# SECRET_KEY=your-secret-key
# SENDGRID_API_KEY=your-sendgrid-api-key
# ALLOWED_HOSTS=localhost,127.0.0.1

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'debug.log',
        },
    },
    'root': {
        'handlers': ['console', 'file'] if DEBUG else ['file'],
        'level': 'DEBUG' if DEBUG else 'WARNING',
    },
}


# Email backend configuration
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

# Additional optional settings:
SENDGRID_SANDBOX_MODE_IN_DEBUG = False  # Set to True for testing without sending emails
SENDGRID_ECHO_TO_STDOUT = True  # For logging emails in the console during development

# Default FROM email
DEFAULT_FROM_EMAIL = os.getenv("MAIL_USERNAME")  # Use the email from your .env
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",") if os.getenv("ALLOWED_HOSTS") else []



# Static and Media Files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Folder for static files in production
STATICFILES_DIRS = [BASE_DIR / 'static']  # Additional static files for development

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  # Folder for uploaded media files

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# SendGrid Email Configuration

EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_PORT = 587  # For TLS

EMAIL_USE_TLS = True
EMAIL_HOST_USER = "apikey"  # This is set by SendGrid
EMAIL_HOST_PASSWORD = os.getenv("SENDGRID_API_KEY")  # Ensure this is set in your .env file

# Background Tasks settings
BACKGROUND_TASK_RUN_ASYNC = True  # Runs tasks asynchronously


