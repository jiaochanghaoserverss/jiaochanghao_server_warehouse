
"""
Service 基类
"""

from django.conf import settings
from common.exceptions import ParamError


class BaseService:

    model = None

    @staticmethod
    def get_object_or_none(model, *args, **kwargs):
        try:
            return model.objects.get(*args, **kwargs)
        except:
            raise None

    @classmethod
    def getby_id(cls, pk: int, raise_exception=False):
        obj = cls.model.objects.get_or_none(pk=pk)
        if not obj and raise_exception:
            raise ParamError('数据未找到')
        return obj

    @classmethod
    def get_mine_by_id(cls, account_id, pk):
        """根据id 和用户查， 防止非法调用"""
        return cls.model.objects.get_or_none(pk=pk, account_id=account_id)

    @staticmethod
    def format_price(price):
        return "{:.2f}".format(price / 100)

    @staticmethod
    def is_empty(obj):
        return obj is None or obj == ""



