from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

SECURE_CONTENT_TYPE_NOSNIFF = True

SECRET_KEY = 'django-insecure-%z)og3_ohsi)25y)fj=m!+!=04!xfu3#uizmvut81y_o#=u131'

DEBUG = True

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_WHITELIST = ['https://mrgerber91-utility-billing-690d.twc1.net']
CSRF_TRUSTED_ORIGINS = ['https://mrgerber91-utility-billing-690d.twc1.net']
CORS_ALLOWED_ORIGINS = ['https://mrgerber91-utility-billing-690d.twc1.net']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'billing.apps.BillingConfig',
    'rest_framework',
    'captcha',
    'compressor',
    'sslserver',
    'corsheaders',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'csp.middleware.CSPMiddleware',
    'corsheaders.middleware.CorsMiddleware',

]

CSP_DEFAULT_SRC = (
    "'self'",
    'https://mrgerber91-utility-billing-690d.twc1.net',
    'https://s3.timeweb.cloud',
    'https://a43db249-billing.s3.timeweb.cloud',  # Добавлен новый источник
)

CSP_STYLE_SRC = (
    "'self'",
    "'unsafe-inline'",
    'https://fonts.googleapis.com',
    'https://cdnjs.cloudflare.com',
    'https://s3.timeweb.cloud',
    'https://a43db249-billing.s3.timeweb.cloud',
)


CSP_FONT_SRC = (
    "'self'",
    'https://fonts.gstatic.com',
    'https://s3.timeweb.cloud',
    'https://a43db249-billing.s3.timeweb.cloud',  # Добавлен новый источник
)

CSP_SCRIPT_SRC = (
    "'self'",
    'https://use.fontawesome.com',
    'https://cdnjs.cloudflare.com',
    'https://a43db249-billing.s3.timeweb.cloud',  # Добавлен новый источник
)

CSP_IMG_SRC = (
    "'self'",
    'https://s3.timeweb.cloud',
    'https://a43db249-billing.s3.timeweb.cloud',  # Добавлен новый источник
)

ROOT_URLCONF = 'utility_billing.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'utility_billing.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s - %(levelname)s - %(message)s',
        },
    },

    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs.log',
            'formatter': 'simple',
        },
    },

    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

AXES_FAILURE_LIMIT = 50000
AXES_COOLOFF_TIME = 0.001
AXES_LOCKOUT_TEMPLATE = 'lockout.html'

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_SAMESITE = 'Strict'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

COMPRESS_ENABLED = True
COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter', 'compressor.filters.cssmin.CSSMinFilter']
COMPRESS_JS_FILTERS = ['compressor.filters.jsmin.JSMinFilter']

AUTHENTICATION_BACKENDS = [

    'django.contrib.auth.backends.ModelBackend'
]

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
AWS_S3_ENDPOINT_URL = 'https://s3.timeweb.cloud'
AWS_S3_CUSTOM_DOMAIN = 'a43db249-billing.s3.timeweb.cloud'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
