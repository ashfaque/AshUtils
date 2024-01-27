[![License: GNU GPLv3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/ashfaque/AshUtils/blob/main/LICENSE)



## How to install
```sh
pip install AshUtils
```



## Documentation
- @cache_response_redis is a django specific decorator, works with get or list method of a class based DRF view. Used to cache the API response in Redis with a default timeout of 5 mins. which can be overridden.
    ```python
    # Add this in settings.py file
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/1",    # Adjust this based on your Redis configuration    # "redis://username:password@127.0.0.1:6379",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        }
    }

    # Usage:-

    from AshUtils import cache_response_redis

    @cache_response_redis(timeout=15, key_prefix='API_NAME_AS_PREFIX_USED_IN_CACHE_KEY')    # ? cache_response_redis decorator should be used only for GET API's get or list method. And it should be the top most decorator.
    @sample_decorator
    def get(self, request, *args, **kwargs):
        response = super(__class__, self).get(self, request, args, kwargs)
        return response
    ```



## License
[GNU GPLv3](LICENSE)
