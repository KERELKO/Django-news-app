from typing import Optional, Any
from django.core.cache import cache
from django.conf import settings


def get_cache(key: str, **kwargs) -> Optional[Any]:
    """
    Simple function to get cache from the cache framework,
    you can pass kwargs to the key to get needed cache
    """
    cache_result = cache.get(key.format(**kwargs))
    return cache_result


def set_cache(
    key: str,
    value: Any,
    time: int = settings.DEFAULT_CACHE_TIMEOUT,
    **kwargs,
) -> None:
    """
    Simple function that set cache,
    you don't have to pass time argument,
    since it uses default settings cache timeout
    """
    cache.set(key.format(**kwargs), value, time)
