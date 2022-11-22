#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
@author: qiyong.zhao
@date: 2014-07-14
@brief: 网站使用的通用组件函数
'''

import urllib.request, urllib.parse, urllib.error

'''
@brief: 生成分页所需的数据结构
@param total: 总数量
@param page: 当前页码
@param pn: 每页数量
@param viewName, kargs: 传给reverse生成url的参数
@param getParams: GET参数
'''
def get_page_struct(total, page, pn, viewName, kwargs=None, getParams=None):
    if total <= pn:
        return None
    try:
        from django.urls import reverse
    except ImportError:
        from django.core.urlresolvers import reverse
    num = int((total + pn - 1)/pn)
    ret = {'total': total, 'page': page, 'pn': pn, 'num': num}
    if not kwargs:
        kwargs = {}
    url_values = ''
    if getParams:
        url_values = urllib.parse.urlencode(getParams)
    if page > 1:
        kwargs['page'] = page - 1
        ret['prev_url'] = reverse(viewName, kwargs=kwargs)
        if url_values:
            ret['prev_url'] += ('?' + url_values)
    if page < num:
        kwargs['page'] = page + 1
        ret['next_url'] = reverse(viewName, kwargs=kwargs)
        if url_values:
            ret['next_url'] += ('?' + url_values)

    begin = page - 3
    if begin < 1:
        begin = 1
    end = begin + 6
    if end > num:
        end = num
    urls = []
    for i in range(begin, end+1):
         kwargs['page'] = i
         url = reverse(viewName, kwargs=kwargs)
         if url_values:
             url += ('?' + url_values)
         urls.append({'page':i, 'url':url})
    ret['urls'] = urls
    return ret


'''
@brief: 根据id从数据库加载更详细的信息
@param dataList: 数据列表
@param model: 模型对象
@param idKey: 在数据列表中id的字段名
@param infoKey: 在数据列表中info的字段名
@param fields: 指定补充的字段列表
'''
def patch_info_by_id_from_db(dataList, model, idKey, infoKey=None, fields=None):
    ids = set()
    for r in dataList:
        id = r.get(idKey)
        if id:
            ids.add(id)
    if not ids:
        return
    if fields:
        if 'id' not in fields:
            fields.append('id')
        infos = model.objects.filter(id__in=ids).values(*fields)
    else:
        infos = list(model.objects.filter(id__in=ids).values())
    for r in dataList:
        id = r.get(idKey)
        if not id:
            continue
        for u in infos:
            if id == u['id']:
                if infoKey is None:
                    r.update(u)
                else:
                    r[infoKey] = u
                break
    return

'''
@brief: 根据code从数据库获取多个数据
@param codes: code列表
@param model: 模型对象
@param returnType: 返回数据实体类型，默认是dict，否则返回object
@param fields: 指定返回的字段列表，在returnType为dict时才会使用该字段，None表示全部字段
@return: dict, code->data
'''
def get_data_by_codes_from_db(codes, model, returnType='dict', fields=None):
    if not codes:
        return {}
    rs = model.objects.filter(code__in=codes)
    if returnType == 'dict':
        if fields:
            if 'code' not in fields:
                fields.append('code')
            rs = rs.values(*fields)
        else:
            rs = list(rs.values())
    rd = {}
    for r in rs:
        if returnType == 'dict':
            rd[r['code']] = r
        else:
            rd[r.code] = r
    return rd

'''
@brief: 根据code从数据库获取多个数据，返回的数据保持传入id的顺序
@param codes: codes列表
@param model: 模型对象
@param returnType: 返回数据实体类型，默认是dict，否则返回object
@param fields: 指定返回的字段列表，在returnType为dict时才会使用该字段，None表示全部字段
@return: list, 保持codes的顺序
'''
def get_data_by_codes_from_db_ordered(codes, model, returnType='dict', fields=None):
    rs = []
    rd = get_data_by_codes_from_db(codes, model, returnType, fields)
    for code in codes:
        r = rd.get(code)
        if not r:
            continue
        rs.append(r)
    return rs


'''
@brief: 根据id从数据库获取多个数据
@param ids: id列表
@param model: 模型对象
@param returnType: 返回数据实体类型，默认是dict，否则返回object
@param fields: 指定返回的字段列表，在returnType为dict时才会使用该字段，None表示全部字段
@return: dict, id->data
'''
def get_data_by_ids_from_db(ids, model, returnType='dict', fields=None):
    if not ids:
        return {}
    rs = model.objects.filter(id__in=ids)
    if returnType == 'dict':
        if fields:
            rs = rs.values(*fields)
        else:
            rs = list(rs.values())
    rd = {}
    for r in rs:
        if returnType == 'dict':
            rd[r['id']] = r
        else:
            rd[r.id] = r
    return rd

'''
@brief: 根据id从数据库获取多个数据，返回的数据保持传入id的顺序
@param ids: id列表
@param model: 模型对象
@param returnType: 返回数据实体类型，默认是dict，否则返回object
@param fields: 指定返回的字段列表，在returnType为dict时才会使用该字段，None表示全部字段
@return: list, 保持ids的顺序
'''
def get_data_by_ids_from_db_ordered(ids, model, returnType='dict', fields=None):
    rs = []
    rd = get_data_by_ids_from_db(ids, model, returnType, fields)
    for id in ids:
        r = rd.get(id)
        if not r:
            continue
        rs.append(r)
    return rs

def is_weixin_browser(request):
    agent = request.META.get('HTTP_USER_AGENT', None)
    if not agent:
        return False
    agent = agent.lower()
    if agent.find('micromessenger') >= 0:
        return True
    return False

def is_android_browser(request):
    agent = request.META.get('HTTP_USER_AGENT', None)
    if not agent:
        return False
    agent = agent.lower()
    if agent.find('huochai') >= 0:
        return True
    return False

def is_huochai_app_browser(request):
    agent = request.META.get('HTTP_USER_AGENT', None)
    if not agent:
        return False
    agent = agent.lower()
    if agent.find('huochai') >= 0:
        return True
    return False

def is_mobile_browser(request):
    import re
    reg_mobile_b = re.compile(r"(android|bb\\d+|meego).+mobile|avantgo|bada\\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od|ad)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino", re.I|re.M)
    reg_mobile_v = re.compile(r"1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\\-(n|u)|c55\\/|capi|ccwa|cdm\\-|cell|chtm|cldc|cmd\\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\\-s|devi|dica|dmob|do(c|p)o|ds(12|\\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\\-|_)|g1 u|g560|gene|gf\\-5|g\\-mo|go(\\.w|od)|gr(ad|un)|haie|hcit|hd\\-(m|p|t)|hei\\-|hi(pt|ta)|hp( i|ip)|hs\\-c|ht(c(\\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\\-(20|go|ma)|i230|iac( |\\-|\\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\\/)|klon|kpt |kwc\\-|kyo(c|k)|le(no|xi)|lg( g|\\/(k|l|u)|50|54|\\-[a-w])|libw|lynx|m1\\-w|m3ga|m50\\/|ma(te|ui|xo)|mc(01|21|ca)|m\\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\\-2|po(ck|rt|se)|prox|psio|pt\\-g|qa\\-a|qc(07|12|21|32|60|\\-[2-7]|i\\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\\-|oo|p\\-)|sdk\\/|se(c(\\-|0|1)|47|mc|nd|ri)|sgh\\-|shar|sie(\\-|m)|sk\\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\\-|v\\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\\-|tdg\\-|tel(i|m)|tim\\-|t\\-mo|to(pl|sh)|ts(70|m\\-|m3|m5)|tx\\-9|up(\\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\\-|your|zeto|zte\\-", re.I|re.M)

    user_agent = request.META.get('HTTP_USER_AGENT', '')
    if not user_agent:
        return False
    if reg_mobile_b.search(user_agent):
        return True
    if reg_mobile_v.search(user_agent[0:4]):
        return True
    return False

'''
@brief: 根据id从字典加载更详细的信息
@param dataList: 数据列表
@param dataDict: 附加字典
@param idKey: 在数据列表中id的字段名
@param infoKey: 在数据列表中info的字段名
@param fields: 指定补充的字段列表
@param force_update: 若infoKey==None 且 字段已存在, 则覆盖更新该字段
'''
def patch_info_by_id_from_dict(dataList, dataDict, idKey, infoKey=None, fields=None, force_update=True):
    for r in dataList:
        _id = r.get(idKey)
        if not _id:
            continue
        try:
            d = dataDict[_id]
        except:
            continue
        if fields:
            patch = {k:v for k,v in d.items() if k in fields}
        else:
            patch = d
        if infoKey is None:
            if force_update:
                r.update(patch)
            else:
                for k, v in patch.items():
                    if k not in r:
                        r[k] = v
        else:
            r[infoKey] = patch
