from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse


__all__ = ('QldPageNumberPagination',)


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


class QldPageNumberPagination(PageNumberPagination):
    page_query_param = 'pageNo'
    page_size = 20
    page_size_query_param = 'pageSize'
    template = None

    def get_paginated_response(self, data):
        page_count = int((self.page.paginator.count - 1) / self.page.paginator.per_page) + 1
        pagination = {
            'total': self.page.paginator.count,
            'pageNo': self.page.number,
            'pageSize': self.page.paginator.per_page,
            'pageCount': page_count,
        }
        return get_response(data, pagination)
