'''
    Author : Ashfaque Alam
    Date : January 27, 2024
    Django Specific Code: Used to cache the API Response in Redis.
'''

from functools import wraps

try:
    # import django
    # from django.conf import settings
    # from rest_framework.decorators import action
    from django.core.cache import cache
    from rest_framework.response import Response
except ImportError as e:
    raise ImportError("Please install Django and djangorestframework first using 'pip install Django djangorestframework'.")


def generate_cache_key(url, kwargs, query_params, user_id):
    # Construct the cache key using provided information
    key_parts = [
        f'url-{url}',    # Using `-` as a secondary delimiter in the cache key.
        f'kwargs-{kwargs}',
        f'qparams-{query_params}',
        f'user-{user_id}',
    ]
    # return f'{api_name}:' + ','.join(key_parts)
    return '|'.join(key_parts)    # Using `|` as the primary delimiter in the cache key.


def cache_response(timeout=60 * 5, key_prefix=''):    # * Default: 5 mins. `timeout` in seconds.
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(view, request, *args, **kwargs):
            url = request.build_absolute_uri()
            # kwargs = kwargs    # ['pk'] if 'pk' in self.kwargs else None
            # kwargs = kwargs.get('pk', {})    # This only fetches 'pk' in the kwargs.
            query_params = request.query_params.urlencode()
            user_id = request.user.id if request.user.is_authenticated else 'anonymous'

            cache_key = generate_cache_key(url, kwargs, query_params, user_id)

            cached_response = cache.get(cache_key)
            if cached_response:
                # print('-------RESPONSE RETURNED FROM CACHE-----')
                return Response(cached_response)    # cached_response holds OrderedDict response.data.

            # print('-------RESPONSE RETURNED FROM DB-----')

            response = view_func(view, request, *args, **kwargs)

            cache.set(cache_key, response.data, timeout=timeout)

            return response
        return _wrapped_view
    return decorator


'''
    ENDS
'''


