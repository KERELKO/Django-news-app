import os
import redis
from .main import *


DEBUG = False

ADMINS = [
	('Kyryl Barabash', 'kerelkobarabash@gmail.com'),
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': 5432,
    }
}

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': [
            os.getenv('REDIS_LOCATION'),  
        ],
    }
}

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_DB = os.getenv('REDIS_DB')
REDIS_PORT = os.getenv('REDIS_PORT')

DEFAULT_REDIS_CLIENT = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB
)

CELERY_ENV = 'core.settings.prod'
