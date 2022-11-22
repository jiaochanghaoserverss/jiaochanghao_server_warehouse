#redis 存储数据
from django_redis import get_redis_connection
def get_redis_conn():
    conn = get_redis_connection()
    return conn