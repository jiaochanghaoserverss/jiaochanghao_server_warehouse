# -*- coding: utf-8 -*-
'''
Dump things to screen.
'''

def obj2dict(obj):
    d = {}
    try:
        d['__class__'] = obj.__class__.__name__
        d['__module__'] = obj.__module__
        d.update(obj.__dict__)
    except:
        d['__str__'] = str(obj)
    return d

def dump_json(data, filePath=None):
    import json
    strJson = json.dumps(data, default=obj2dict, sort_keys=True, indent=4,  ensure_ascii=False)
    if filePath:
        fp = open(filePath, 'wb')
        fp.write(strJson)
    return strJson
