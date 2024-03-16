import redis
from .main import * 


DEBUG = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

ALLOWED_HOSTS = ['*']

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
DEFAULT_CACHE_TIMEOUT = 1 * 15

# Redis
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

CELERY_ENV = 'backend.core.setting.local'
