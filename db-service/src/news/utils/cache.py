from typing import Callable
from django.core.cache import cache
from rest_framework.response import Response


def cache_response(timeout: int = 60):  # До лучших времен
    """
    Кастомный декоратор для кеширования http ответа.
    """
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            request = args[0]
            key = f"{request.method}.{request.path}?{request.query_params.urlencode()}"
            if response_from_cache := cache.get(key):
                return Response(response_from_cache)

            response = func(*args, **kwargs)
            cache.set(key, response.data, timeout)
            return response

        return wrapper
    return decorator
