# -*- coding: utf-8 -*-

import abc


class BaseServiceRegistry(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def register(self, key, value):
        """
        注册服务
        :param key      服务名
        :param value    服务数值
        :return         当前服务索引
        :rtype          int
        """
        return 0

    # @abc.abstractmethod
    # def unregister(self, key, value):
    #     """
    #     取消服务
    #     :param key      服务名
    #     :param value    服务数值
    #     """

    # @abc.abstractmethod
    # def heart_beat(self, key, value):
    #     """
    #     服务心跳
    #     :param key      服务名
    #     :param value    服务数值
    #     """


class RedisServiceRegistry(BaseServiceRegistry):

    def __init__(self, redis_client):
        self._redis_client = redis_client

    def register(self, key, value):
        # client = self._redis_client
        # with client.pipeline() as pipe:
        #     pipe.watch(key)
        #     total = pipe.hlen(key)
        #     pipe.hsetnx(key, value, total + 1)
        #     ret = pipe.hget(key, value)
        #     pipe.execute()
        #     return ret
        client = self._redis_client
        total = client.hlen(key)
        client.hsetnx(key, value, total + 1)
        ret = client.hget(key, value)
        return ret



