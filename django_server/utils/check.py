from functools import wraps
import json
import jwt
from django.conf import settings
from django.http import HttpResponse
from apps.auths.models import User


def request_verify(request_method: str, need_params=None):
    """
        在views方法上加装饰器 例如：@request_verify('get', ['id'])
        :param request_method:
        :param need_params:
        :return:
    """

    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            method = str(request.method).lower()
            # 先判断类型，类型不符合，直接return
            if request_method and not method == request_method.lower():
                response = "method {0} not allowed for: {1}".format(request.method, request.path)
                return response_failure(response)

            request.params = {}
            # 暂时不用get请求传参，get的情况可以先忽略
            if method == 'get':
                if not request.GET:
                    if need_params:
                        response = "缺少参数"
                        return response_failure(response)
                else:
                    params = {}
                    request_params = request.GET
                    for item in request_params:
                        params.update({item: request_params.get(item)})
                    # get 必填参数校验
                    if need_params:
                        for need_param_name in need_params:
                            if not params.get(need_param_name):
                                response = "参数 {0} 不能为空".format(need_param_name)
                                return response_failure(response)
                    request.params = params
            else:  # method == post
                if not request.body or request.body == {}:  # 参数为空的情况下
                    if need_params:  # 验证必传
                        response = "缺失参数"
                        return response_failure(response)
                else:  # 非空的时候，尝试去获取参数
                    try:
                        real_request_params = json.loads(request.body)  # 这边要try一下，如果前端传参不是json，json.loads会异常
                    except Exception as e:
                        response = "参数格式不合法"
                        return response_failure(response)
                    # 取出来以后再去判断下必填项是否每一项都有值
                    if need_params:
                        for need_param_name in need_params:
                            if not real_request_params.get(need_param_name):
                                # 如果必传参数取出来是'' (PS: 没传和传了''通过get取出来都是'')，就抛出
                                response = "参数 {0} 不能为空".format(need_param_name)
                                return response_failure(response)
                    # 一直到这里都无异常那么就可以把参数塞进request对象了，避免view里还要再去json.loads
                    request.params = real_request_params
            return func(request, *args, **kwargs)

        return inner

    return decorator


# 校验结果封装

def response_success(message, data=None, data_list=None):
    return HttpResponse(json.dumps({
        'code': 200,  # code由前后端配合指定
        'message': message,  # 提示信息
        'success': True,  # 返回单个对象
        'data': data,  # 返回单个对象
        'dataList': data_list  # 返回对象数组
    }, ensure_ascii=False), 'application/json')

def response_failure(message):
    return HttpResponse(json.dumps({
        'code': 500,
        'message': message,
        'success': False
    }, ensure_ascii=False), 'application/json')

def response_page_success(message, data=None, data_list=[], total=None, page=None, pageSize=None):
    return HttpResponse(json.dumps({
        'success': True,
        'code': 200,  # code由前后端配合指定
        'message': message,  # 提示信息
        'data': data,  # 返回单个对象
        'dataList': data_list,  # 返回对象数组
        'total': total,  # 记录总数
        'page': page,  # 当前页面
        'pageSize': pageSize  # 当前页面分页大小
    }, ensure_ascii=False), 'application/json')


# 登入凭证装饰器
def token_required():
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            try:
                auth = request.META.get('HTTP_AUTHORIZATION').split("_")
            except AttributeError:
                return response_failure("No authenticate header")

            if auth[0].lower() == 'token':
                try:
                    dict = jwt.decode(auth[1], settings.SECRET_KEY, algorithms=['HS256'])
                    username = dict.get('data').get('name')
                except jwt.ExpiredSignatureError:
                    return response_failure("Token expired")
                except jwt.InvalidTokenError:
                    return response_failure("Invalid token")
                except Exception as e:
                    return response_failure("Can not get user object")

                try:
                    user = User.objects.get(name=username)
                except User.DoesNotExist:
                    return response_failure("User Does not exist")

                return view_func(request, *args, **kwargs)
            else:
                return response_failure("Error authenticate header")

        return _wrapped_view

    return decorator
