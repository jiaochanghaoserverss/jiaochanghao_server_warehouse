# -*- coding: utf-8 -*-
import hashlib


def md5(val):
    return hashlib.md5(val).hexdigest()


def get_file_md5(file_data: bytes):
    """
    获取小文件的md5
    """
    md5_obj = hashlib.md5()
    md5_obj.update(file_data)
    return md5_obj.hexdigest()
