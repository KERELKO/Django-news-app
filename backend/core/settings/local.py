import redis
from .main import * 


DEBUG = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

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

DEFAULT_CACHE_TIMEOUT = 5 * 60

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': [
            'redis://127.0.0.1:6379',  # leader
        ],
    }
}

AUTH_PASSWORD_VALIDATORS = []

REDIS_HOST = 'localhost'
REDIS_DB = 1 
REDIS_PORT = 6379

DEFAULT_REDIS_CLIENT = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB
)
