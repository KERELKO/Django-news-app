from typing import Optional
from django.core.cache import cache
from django.conf import settings


def get_cache(key: str, **kwargs) -> Optional['cache']:
	cache_result = cache.get(key.format(**kwargs))
	return cache_result


def set_cache(
	key: str, 
	value: any,  
	time: int = settings.DEFAULT_CACHE_TIMEOUT,
	**kwargs
) -> None:
	cache.set(key.format(**kwargs), value, time)
