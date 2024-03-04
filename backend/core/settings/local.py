import redis
from .main import * 


DEBUG = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

ALLOWED_HOSTS = ['*']

STATIC_URL = 'static/'
STATIC_ROOT = BASE_FRONTEND_DIR / 'static/'

MEDIA_URL = 'images/'
MEDIA_ROOT = STATIC_ROOT / 'images'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'news',
        'USER': 'news',
        'PASSWORD': 'news',
    }
}

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': [
            'redis://127.0.0.1:6379',  # leader
        ],
    }
}

DEFAULT_CACHE_TIMEOUT = 1 * 60

REDIS_HOST = 'localhost'
REDIS_DB = 1 
REDIS_PORT = 6379

DEFAULT_REDIS_CLIENT = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB
)

AUTH_PASSWORD_VALIDATORS = []

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

CELERY_ENV = 'core.settings.local'
