"""
Django settings for avengers_cart project.
Production-ready with Render deployment support.
"""

import os
from pathlib import Path
from decouple import config

# ═══════════════════════════════════════════
# BASE
# ═══════════════════════════════════════════
BASE_DIR = Path(__file__).resolve().parent.parent


# ═══════════════════════════════════════════
# SECURITY
# ═══════════════════════════════════════════
SECRET_KEY = config(
    'SECRET_KEY',
    default='django-insecure-dev-key-change-in-production'
)

DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = ['*']

# CSRF trusted origins (HTTPS domains)
CSRF_TRUSTED_ORIGINS = [
    'https://codealpha-mystore-bs7k.onrender.com',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]


# ═══════════════════════════════════════════
# APPLICATIONS
# ═══════════════════════════════════════════
INSTALLED_APPS = [
    'jazzmin',                                  # Must be before admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'store',                                    # Our app
]


# ═══════════════════════════════════════════
# MIDDLEWARE
# ═══════════════════════════════════════════
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',   # Static files in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ═══════════════════════════════════════════
# URLS & WSGI
# ═══════════════════════════════════════════
ROOT_URLCONF = 'avengers_cart.urls'

WSGI_APPLICATION = 'avengers_cart.wsgi.application'


# ═══════════════════════════════════════════
# TEMPLATES
# ═══════════════════════════════════════════
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
                'store.context_processors.cart_counter',      # Custom: cart badge
            ],
        },
    },
]


# ═══════════════════════════════════════════
# DATABASE
# ═══════════════════════════════════════════
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ═══════════════════════════════════════════
# PASSWORD VALIDATION
# ═══════════════════════════════════════════
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ═══════════════════════════════════════════
# INTERNATIONALIZATION
# ═══════════════════════════════════════════
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ═══════════════════════════════════════════
# STATIC FILES (CSS, JS, Images)
# ═══════════════════════════════════════════
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'store' / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise for production static file serving
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ═══════════════════════════════════════════
# MEDIA FILES (User uploads)
# ═══════════════════════════════════════════
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ═══════════════════════════════════════════
# AUTHENTICATION
# ═══════════════════════════════════════════
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'


# ═══════════════════════════════════════════
# DEFAULT AUTO FIELD
# ═══════════════════════════════════════════
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ═══════════════════════════════════════════
# JAZZMIN SETTINGS
# ═══════════════════════════════════════════
JAZZMIN_SETTINGS = {
    "site_title": "My Store Admin",
    "site_header": "My Store",
    "site_brand": "My Store",
    "site_logo": None,
    "login_logo": None,
    "site_logo_classes": "img-circle",
    "site_icon": None,
    "welcome_sign": "Welcome to My Store Admin Panel",
    "copyright": "My Store Ltd",
    "search_model": [],

    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Store Front", "url": "/", "new_window": True},
        {"model": "auth.User"},
        {"app": "store"},
    ],

    "usermenu_links": [
        {"name": "Store Front", "url": "/", "new_window": True},
        {"model": "auth.user"},
    ],

    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],

    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "store.Category": "fas fa-tags",
        "store.Product": "fas fa-box",
        "store.Cart": "fas fa-shopping-cart",
        "store.CartItem": "fas fa-cart-plus",
        "store.Order": "fas fa-shopping-bag",
        "store.OrderItem": "fas fa-receipt",
        "store.Review": "fas fa-star",
        "store.Profile": "fas fa-user-circle",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    "related_modal_active": False,
    "custom_css": None,
    "custom_js": None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs"
    },
    "language_chooser": False,
}


# ═══════════════════════════════════════════
# JAZZMIN UI TWEAKS
# ═══════════════════════════════════════════
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-danger",
    "accent": "accent-danger",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-danger",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}