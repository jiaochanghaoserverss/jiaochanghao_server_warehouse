# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import CharField, ForeignKey
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


__all__ = ('RemoteIdField', 'FileIdField', 'SimpleForeignKey')


class RemoteIdField(CharField):
    max_length = 64
    description = _("RemoteId (up to %(max_length)s)")

    def __init__(self, **kwargs):
        kw = kwargs.copy()
        kw['max_length'] = RemoteIdField.max_length
        kw['default'] = ''
        kw['blank'] = True
        kw['null'] = False
        super(RemoteIdField, self).__init__(**kw)


class FileIdField(CharField):
    max_length = 255
    description = _("RemoteId (up to %(max_length)s)")

    def __init__(self, **kwargs):
        kw = kwargs.copy()
        self.file_url_key = kw.pop('file_url_key', None)
        self.file_url_host = kw.pop('file_url_host', None) or settings.FILE_CDN_DOMAIN
        kw['max_length'] = kw.pop('max_length', None) or self.__class__.max_length
        kw['default'] = ''
        kw['blank'] = True
        kw['null'] = False
        super().__init__(**kw)


class SimpleForeignKey(ForeignKey):
    """
    默认外键字段, 没有外键约束, 有外键索引
    """
    on_delete = models.DO_NOTHING
    db_constraint = False

    def __init__(self, to, **kwargs):
        _cls = self.__class__
        kw = kwargs.copy()
        kw['on_delete'] = _cls.on_delete
        kw['db_constraint'] = _cls.db_constraint
        super().__init__(to, **kw)
