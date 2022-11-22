from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from rest_framework import views, status, mixins
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.serializers import IntegerField
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet


class RowDict(dict):
    """A dict that allows for object-like property access syntax."""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            return None


def get_response(context=None, pagination=None, code=None, message=None,
                 http_status=status.HTTP_200_OK, headers=None):
    if http_status >= status.HTTP_400_BAD_REQUEST:
        data = {
            'code': code,
            'message': message
        }
    else:
        data = {
            'data': context
        }
        if pagination:
            data['pagination'] = pagination
    return Response(data=data, status=http_status, headers=headers, template_name=None)


def get_response_in_middleware(context=None, pagination=None, code=None, message=None, http_status=status.HTTP_200_OK,
                               headers=None):
    if http_status >= status.HTTP_400_BAD_REQUEST:
        data = {
            'code': code,
            'message': message
        }
    else:
        data = {
            'data': context
        }
        if pagination:
            data['pagination'] = pagination
    response = JsonResponse(data=data, status=http_status)
    if headers:
        for name, value in headers.items():
            response[name] = value
    return response


class BaseParam(Serializer):
    """利用serializer 做参数校验"""

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class PageParam(BaseParam):
    page_no = IntegerField(required=False, default=1)
    page_size = IntegerField(required=False, default=5)


class IdParam(BaseParam):
    object_id = IntegerField(required=True)


class _MyView:

    @staticmethod
    def valid_param(param: BaseParam, raise_exception=True) -> RowDict:
        param.is_valid(raise_exception=raise_exception)
        return RowDict(param.validated_data)

    @staticmethod
    def id_param(data: dict, raise_exception=True) -> int:
        param = IdParam(data=data)
        param.is_valid(raise_exception=raise_exception)
        return param.validated_data.get('object_id')

    @staticmethod
    def success_response(data=None, message=''):
        return Response(dict(success=True, message=message, data=data))

    @staticmethod
    def fail_response(msg="Failed", data=None, code=0):
        return Response(data=dict(success=False, code=code, message=msg, data=data), status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def do_response(flag, message='', data=None):
        if flag:
            return Response(dict(success=True, message=message, data=data))
        else:
            return Response(data=dict(success=False, message=message, data=data),
                            status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def html_response(data, template):
        return Response(content_type='text/html', template_name=template)

    @classmethod
    def get_page_param(cls, request):
        try:
            page = request.query_params.get("pageNo", 1)
        except:
            page = 1
        try:
            page_size = request.query_params.get("pageSize", 15)
        except:
            page_size = 15
        return page, page_size

    def fill_result(self, data):
        pass

    def custom_filter(self, request, queryset):
        """子类可重写"""
        return queryset


class BaseApiView(views.APIView, _MyView):
    """基础API View"""
    pass


class BaseListApiView(ListAPIView, _MyView):
    pass


class PermLessListApiView(ListAPIView, _MyView):
    permission_classes = (AllowAny,)


class PermLessApiView(BaseApiView):
    """
    无需登录接口
    """
    permission_classes = (AllowAny,)


class BaseModelViewSet(ModelViewSet, _MyView):
    edit_serializer_class = None
    full_result = None
    user_id = None
    action_roles_authenticated = None

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.success_response(serializer.data)

    def create(self, request, *args, **kwargs):
        _data = request.data
        _data['creator'] = request.user_id
        serializer = self.get_edit_serializer(data=_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return self.success_response(data=serializer.data)

    def update(self, request, *args, **kwargs):
        _data = request.data
        _data['latest_editor'] = request.user_id
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_edit_serializer(instance, data=_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return self.success_response()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = self.custom_filter(request, queryset)

        page, page_size = self.get_page_param(request)
        result = page_query_set(queryset, page=page, page_size=page_size, serializer=self.serializer_class)
        if result.get('data'):
            self.fill_result(result.get('data'))
        return Response(result)

    def get_edit_serializer(self, *args, **kwargs):
        assert self.edit_serializer_class is not None, (
                "'%s' should either include a `serializer_class` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__
        )

        serializer_class = self.edit_serializer_class
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def perform_destroy(self, instance):
        instance.delete()

    def clear_prefetched_cache(self, instance):
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

    def filter_queryset(self, queryset):
        if self.filter_backends is None:
            return queryset
        return super(BaseModelViewSet, self).filter_queryset(queryset)


class ListModelViewSet(mixins.ListModelMixin, GenericViewSet, _MyView):
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = self.custom_filter(request, queryset)

        page, page_size = self.get_page_param(request)
        result = page_query_set(queryset, page=page, page_size=page_size, serializer=self.serializer_class)
        if result.get('data'):
            self.fill_result(result.get('data'))
        return Response(result)


class PermLessModelViewSet(BaseModelViewSet):
    """
    无需登录接口
    """
    permission_classes = (AllowAny,)


class QldPagination(PageNumberPagination):
    """
    rest frame work 分页自定义组件
    """
    page_query_param = 'page'
    page_size = 15
    page_size_query_param = 'page_size'
    template = None

    def get_paginated_response(self, data):
        page_count = int((self.page.paginator.count - 1) / self.page.paginator.per_page) + 1
        pagination = {
            'total': self.page.paginator.count,
            'page': self.page.number,
            'page_count': page_count
        }
        return get_response(data, pagination)


def page_query_set(query_set, page=1, page_size=15, serializer=None):
    if isinstance(query_set, list):
        counts = len(query_set)
    else:
        counts = query_set.count()
    try:
        page_size = int(page_size)
    except (TypeError, ValueError):
        raise PageNotAnInteger('That page_size number is not an integer')
    paginator = Paginator(query_set, page_size)
    try:
        entries = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        entries = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        entries = paginator.page(paginator.num_pages)
    page_count = int((counts + page_size - 1) / page_size)
    if serializer:
        entries = serializer(entries, many=True).data
    pagination = dict(total=counts,
                      pageCount=page_count,
                      pageSize=page_size,
                      pageNo=int(page))
    return dict(pagination=pagination, data=entries)
