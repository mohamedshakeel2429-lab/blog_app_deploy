from pathlib import Path
import os
import logging

BASE_DIR = Path(__file__).resolve().parent.parent

# ================= SECURITY =================
SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = False

ALLOWED_HOSTS = [
    "*"
]

# ================= APPS =====================
INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Your app
    'blog',

    # Cloudinary
    'cloudinary',
    'cloudinary_storage',
]

# ================= MIDDLEWARE ================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # Whitenoise for static files
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Your custom middleware
    'myproject.middleware.RedirectAuthenticatedUserMiddleware',
    'myproject.middleware.RedirectNonAuthenticatedUserMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

# ================= TEMPLATES =================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # IMPORTANT FIX
        'DIRS': [
            BASE_DIR / "templates"
        ],

        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'

# ================= DATABASE ==================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('MYSQL_ADDON_DB'),
        'USER': os.environ.get('MYSQL_ADDON_USER'),
        'PASSWORD': os.environ.get('MYSQL_ADDON_PASSWORD'),
        'HOST': os.environ.get('MYSQL_ADDON_HOST'),
        'PORT': os.environ.get('MYSQL_ADDON_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ================= AUTH ======================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ================= I18N ======================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ================= STATIC ====================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ================= MEDIA (CLOUDINARY) ========
CLOUDINARY_STORAGE = {
    "CLOUDINARY_URL": os.getenv("CLOUDINARY_URL")
}

DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# DO NOT USE MEDIA_URL FOR CLOUDINARY
# MEDIA_URL = "/media/"

# ================= EMAIL (MAILTRAP) ==========
DEFAULT_FROM_EMAIL = "your_email@shakeel.com"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = '68e7c151522763'
EMAIL_HOST_PASSWORD = 'af00c755f4d790'

# ================= LOGGING ===================
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
}

