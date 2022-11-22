# -*- coding: utf-8 -*-

import six
import datetime
from urllib.parse import urljoin
from rest_framework import serializers
from common.fields import FileIdField
from rest_framework.fields import ChoiceField, DateTimeField

__all__ = ('BaseSerializer', 'FileIdSerializerField', 'BaseAdminSerializer')


class FileIdSerializerField(serializers.CharField):

    def __init__(self, **kwargs):
        self.file_url_host = kwargs.pop('file_url_host')
        self.file_url_key = kwargs.pop('file_url_key')
        super().__init__(**kwargs)


class FileIDMixin:

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        for field_name, field in self.get_fields().items():
            if isinstance(field, FileIdSerializerField):
                file_url_key = field.file_url_key
                if not file_url_key:
                    file_url_key = field_name.replace('_id', '') + '_url'
                value = ''
                if ret[field_name]:
                    value = urljoin(field.file_url_host, ret[field_name])
                ret[file_url_key] = value
                # ret[field_name] = value
        return ret

    def build_standard_field(self, field_name, model_field):
        field_class, kwargs = super().build_standard_field(field_name, model_field)
        if isinstance(model_field, FileIdField):
            kwargs['file_url_host'] = model_field.file_url_host
            kwargs['file_url_key'] = model_field.file_url_key

        return field_class, kwargs


class ChoiceDisplayField(ChoiceField):
    def __init__(self, *args, **kwargs):
        super(ChoiceDisplayField, self).__init__(*args, **kwargs)
        self.choice_strings_to_display = {
            six.text_type(key): value for key, value in self.choices.items()
        }

    def to_representation(self, value):
        if value is None:
            return value
        return {
            'value': self.choice_strings_to_values.get(six.text_type(value), value),
            'display': self.choice_strings_to_display.get(six.text_type(value), value),
        }


class TimeStampField(serializers.DateTimeField):
    # def to_internal_value(self, data):
    #     epoch = datetime.datetime(1970, 1, 1)
    #     return int((value - epoch).total_seconds())

    def to_representation(self, value):
        if value is None:
            return value
        # 毫秒级别的timestamp
        return int(datetime.datetime.timestamp(value) * 1000)


class CommonBaseSerializer(FileIDMixin, serializers.ModelSerializer):
    serializer_choice_field = ChoiceDisplayField
    serializers.ModelSerializer.serializer_field_mapping[FileIdField] \
        = FileIdSerializerField


class BaseSerializer(CommonBaseSerializer):

    create_time = TimeStampField(read_only=True)
    update_time = TimeStampField()
    last_login = TimeStampField()
    grading_time = TimeStampField()
    audit_time = TimeStampField()
    signed_time = TimeStampField()

    @staticmethod
    def format_price(price):
        return "{:.2f}".format(price / 100)


class BaseAdminSerializer(CommonBaseSerializer):

    create_time = DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    update_time = DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    @staticmethod
    def format_price(price):
        return "{:.2f}".format(price / 100)

