import os
import redis
from .main import *


DEBUG = False

ADMINS = [
    ('Kyryl Barabash', 'kerelkobarabash@gmail.com'),
]

ALLOWED_HOSTS = ['*']

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
REDIS_URL = 'redis://cache:6379'

DEFAULT_REDIS_CLIENT = redis.Redis(
    host='cache',
    port=6379,
    db=1,
)

CACHES['default']['LOCATION'] = REDIS_URL
