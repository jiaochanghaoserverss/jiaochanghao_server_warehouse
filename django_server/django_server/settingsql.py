from .settings import *
# Logger settings
# LOGGING = get_logger(level="INFO", handler="console")
# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases




CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}