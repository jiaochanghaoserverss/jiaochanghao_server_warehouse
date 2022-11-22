# -*- coding: utf-8 -*-
from django.db import models
from common.redis_client import get_snowflake_client

SNOWFLAKE_WORKER_CACHE_KEY = 'snowflake_worker'


def get_snowflake_id_generator():
    from common.utils.snowflakeid import get_worker_id_from_cache, ProcessSnowflakeID
    client = get_snowflake_client()
    worker_id = get_worker_id_from_cache(client, SNOWFLAKE_WORKER_CACHE_KEY)
    return ProcessSnowflakeID(worker_id)


class SnowflakePrimaryField(models.BigIntegerField):
    """
    使用Snowflake ID 作为主键
    """
    snow = get_snowflake_id_generator()

    def __init__(self, **kwargs):
        kw = kwargs.copy()
        kw['default'] = self.snow.next
        kw['unique'] = True
        kw['primary_key'] = True
        super().__init__(**kw)
