"""
Django settings for egarage_project project.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-k9!7gkbu++55!=)ye*iv(j1+eqz%3g0)tk1&)ecnt!^nz(!@-n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    "unfold",  # Must be before admin!
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.import_export",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "import_export", 
    "core",
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

ROOT_URLCONF = 'egarage_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'egarage_project.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'egarage_db',
        'USER': 'postgres',
        'PASSWORD': '0312',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- STATIC & MEDIA FILES CONFIG ---

# URL used when referring to static files
STATIC_URL = 'static/'

# Extra places for collectstatic to find custom static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# THE FIX: The directory where collectstatic gathers files for production
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files (for uploaded images/documents)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# --- AUTHENTICATION CONFIG ---

AUTH_USER_MODEL = 'core.User'
LOGIN_REDIRECT_URL = 'dashboard_redirect'
LOGOUT_REDIRECT_URL = 'service_list'


# --- UNFOLD MODERN ADMIN UI CONFIG ---

UNFOLD = {
    "SITE_TITLE": "eGarage Admin",
    "SITE_HEADER": "eGarage Management",
    "THEME": "dark",  # Forces the entire dashboard into dark mode
    "COLORS": {
        "primary": {
            "50": "238 242 255",
            "100": "224 231 255",
            "200": "199 210 254",
            "300": "165 180 252",
            "400": "129 140 248",
            "500": "99 102 241",  # Vibrant Indigo
            "600": "79 70 229",
            "700": "67 56 202",
            "800": "55 48 163",
            "900": "49 46 129",
            "950": "30 27 75",
        },
    },
    "DASHBOARD": {
        "navigation": [
            {
                "title": "Quick Stats",
                "items": [
                    {
                        "title": "Dashboard Home",
                        "link": "admin:index",
                        "icon": "dashboard",
                    },
                ],
            },
        ],
        # Links your admin.py logic to these cards
        "callback": "core.admin.dashboard_callback",
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'