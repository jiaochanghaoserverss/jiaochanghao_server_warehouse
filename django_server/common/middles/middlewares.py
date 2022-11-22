import time
import urllib
import urllib.parse
import logging
import traceback

from django.conf import settings
from django.http import JsonResponse
from django.http.request import HttpRequest

from common.exceptions import BaseError, InternalError, Unauthorized, PermissionDenied
from common.views import get_response_in_middleware
from common.middles.token import JWTUtil, InvalidJWTSign
from apps.auths.service import AccountService


logger = logging.getLogger('logger')


class LoggerMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self._start = 0
        self._query_params = None
        self._data_params = None

    def __call__(self, request):
        response = self.get_response(request)
        exclude = ['']
        if request.method in ["OPTIONS", "HEAD"] or request.path_info in exclude:
            return response

        try:
            user_id = request.user.id
        except AttributeError:
            user_id = 0

        if 400 <= response.status_code <= 499:
            logger.warning('%s | %s | %s | %s | %s | %s | %.2f' %
                           (request.method, user_id, request.path_info, self._query_params, self._data_params,
                            response.status_code, time.time() - self._start))
        else:
            logger.info('%s | %s | %s | %s | %s | %s | %.2f' %
                        (request.method, user_id, request.path_info, self._query_params,
                         self._data_params, response.status_code, time.time() - self._start))
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        self._start = time.time()
        self._query_params = dict(urllib.parse.parse_qsl(urllib.parse.urlencode(request.GET)))
        self._data_params = request.body

        return None


class APIExceptionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, BaseError):
            return self.get_error_response(exception)
        logging.error(traceback.format_exc())
        return self.get_error_response(InternalError('服务器出错了: )'))

    def get_error_response(self, err: BaseError):
        msg = {'code': err.code, "success": False, 'message': err.message}
        if err.status_code == 400:
            logger.error("Get-400-error %s", msg)
            return JsonResponse(msg, status=err.status_code)

        if err.status_code == 500:
            logger.error(err.message)
            logger.error(traceback.format_exc())
        return JsonResponse(msg, status=err.status_code)


def get_user_from_request(request):
    if not hasattr(request, '_cached_user'):
        request._cached_user = AccountService.getby_id(request.payload.user_id)
    return request._cached_user


def is_permission_less_view(view_func):
    init_args = getattr(view_func, 'initkwargs', None)
    if init_args:
        permission_classes = init_args.get('permission_classes', [])
        for p in permission_classes:
            if p.__name__ == 'AllowAny':
                return True
    else:
        try:
            permission_classes = view_func.view_class.permission_classes
            for p in permission_classes:
                if p.__name__ == 'AllowAny':
                    return True
        except:
            return False
    return False


class JWTAuthenticationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

        self._jwt_util = JWTUtil(settings.JWT_SECRET_KEY, settings.JWT_HEADERS)

    def __call__(self, request: HttpRequest):
        response = self.get_response(request)
        return response

    @staticmethod
    def get_user(payload):
        return AccountService.getby_id(payload.user_id)

    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            token = self.get_jwt_token(request)
            skip_token_check = is_permission_less_view(view_func)
            payload = self.get_jwt_payload(token, skip_token_check=skip_token_check)
            self.patch_request(request, payload)
        except BaseError as err:
            code = err.code or 1
            message = err.message or '请先登录'
            return get_response_in_middleware(code=code, message=message, http_status=err.status_code)

    def get_jwt_token(self, request: HttpRequest) -> str:
        token_start_pos = 7  # len("Bearer ")
        token = request.META.get('HTTP_AUTHORIZATION', '')[token_start_pos:]
        return token

    def get_jwt_payload(self, token: str, skip_token_check=False):
        if not token:
            return settings.APP_PAYLOAD()
        try:
            payload = self._jwt_util.decode(token)
        except InvalidJWTSign:
            if skip_token_check:
                return settings.APP_PAYLOAD()
            raise Unauthorized(message='无效token')
        return payload

    def patch_request(self, request, payload):
        request.payload = payload
        if payload and payload.user_id:
            request.is_authenticated = True
            request.user_id = payload.user_id
            # request.user = SimpleLazyObject(lambda: get_user_from_request(request))
        else:
            request.is_authenticated = False
            request.user_id = None
            # request.user = AnonymousUser()


class PermissionMiddleware:
    API_PREFIX = '/api'
    SRV_PREFIX = 'srv'

    SKIP_LOGIN_NAMESPACE = [
        # 'auths',
        # 'wechat',
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if self.is_api(request):
                self.check_login(request, view_func)
        except InternalError as err:
            code = err.code or 1
            message = err.message or ''
            return get_response_in_middleware(code=code, message=message, http_status=err.status_code)

    def is_api(self, request):
        namespace = request.resolver_match.namespace
        if not namespace:
            namespace = request.path
        return namespace.startswith(self.API_PREFIX)

    def check_login(self, request, view_func):
        try:
            # 已登录, 则跳过
            if request.is_authenticated:
                return
            # 如果对应的Namespace允许不登录, 则跳过
            permission_less = is_permission_less_view(view_func)
            if permission_less:
                return

            # 检测到未登录
            message = '未登录'
            return get_response_in_middleware(code=1, message=message, http_status=401)

        except IndexError:
            pass

    def check_admin(self, request):
        if not request.payload.is_admin:
            raise PermissionDenied
