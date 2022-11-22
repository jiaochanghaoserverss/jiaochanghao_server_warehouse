# -*- coding: utf-8 -*-

'''
@brief: import工具
'''
from importlib import import_module

def import_class(path):
    """
    Import class from path.
    """
    mod_name, klass_name = path.rsplit('.', 1)
    try:
        mod = import_module(mod_name)
    except AttributeError as err:
        raise Exception('Error importing {0}: "{1}"'.format(mod_name, err))
    try:
        klass = getattr(mod, klass_name)
    except AttributeError:
        raise Exception('Module "{0}" does not define a "{1}" class'.format(mod_name, klass_name))
    return klass