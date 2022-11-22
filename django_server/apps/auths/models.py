import datetime

import jwt
from django.db import models

# Create your models here.
from django.contrib.auth.hashers import (
    check_password, make_password
)
from common.fields import FileIdField
from common.fields import SimpleForeignKey
from common.models import BaseModel
from django_server import settings


class User(BaseModel):
    account = models.CharField(max_length=10, default='', help_text='账号', unique=True)
    mobile = models.CharField(max_length=32, default='', blank=True, help_text='电话', unique=True)
    email = models.CharField(max_length=32, default='', blank=True, help_text='邮箱', unique=True)
    avatar = FileIdField(help_text='头像', default='', blank=True)
    username = models.CharField(max_length=32, default='', help_text='用户名')
    password = models.CharField(max_length=128, default='')
    last_login = models.DateTimeField(default=None, null=True, blank=True, help_text='最近登录时间')

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        token = jwt.encode({
            'exp': datetime.datetime.now() + datetime.timedelta(days=1),
            'iat': datetime.datetime.now(),
            'data': {
                'account': self.account,
                'id': self.id
            }
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')
    class Meta:
        db_table = 'user'
        verbose_name = verbose_name_plural = '用户信息'

    @staticmethod
    def mk_password(raw_password):
        return make_password(raw_password)

    def set_password(self, raw_password):
        self.password = self.mk_password(raw_password)

    def check_password(self, raw_password):
        """
        Return a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        return check_password(raw_password, self.password)