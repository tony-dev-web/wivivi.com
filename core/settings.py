#import os
SECRET_KEY = ''
DEBUG = False
CSRF_TRUSTED_ORIGINS = ['']

ALLOWED_HOSTS = ['']

INSTALLED_APPS = [
    'django_cassandra_engine',
    #'django_cassandra_engine.sessions',
    'django.contrib.postgres',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'backoffice',
    'annonce',
    'utilisateur',
    'equipe']

MIDDLEWARE = [
    'core.middleware.Midoudou',
    #'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware']

ROOT_URLCONF = 'core.urls'

USER_AGENTS_CACHE = 'default'
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        'KEY_PREFIX': 'cF',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "TIMEOUT": 1209600,
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor"}}}


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['/home/ipk/mvt/templates/'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                #'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


ASGI_APPLICATION = 'core.asgi.application'
WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {'default': {},

        'cas2': {}}


LANGUAGES = [('fr', 'French')]
SECURE_HSTS_PRELOAD = True
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True
CASSANDRA_FALLBACK_ORDER_BY_PYTHON = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = ''
EMAIL_USE_TLS = False
EMAIL_PORT = 587
EMAIL_USE_SSL = True
EMAIL_SSL_CERTFILE = None
EMAIL_SUBJECT_PREFIX = ''
EMAIL_TIMEOUT = None
EMAIL_USE_LOCALTIME = False
PREPEND_WWW = False
LANGUAGE_CODE = 'fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = 'static/'
