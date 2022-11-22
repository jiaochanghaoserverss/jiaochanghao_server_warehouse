# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from common.middles.token import JWTUtil
from common.exceptions import Unauthorized
from apps.auths.service import AccountService

__all__ = ('JWTAppAuthentication',)


class JWTAppAuthentication(BaseAuthentication):
    """
    JWT authentication.

    Clients should authenticate by passing the jwt token key in the "Authorization"
    HTTP header, prepended with the string "Bearer ".  For example:

        Authorization: Bearer 401f7ac837da42b97f613d789819ff93537bee6a
    """

    keyword = 'Bearer'
    jwt_util = JWTUtil(settings.JWT_SECRET_KEY, settings.JWT_HEADERS)

    @staticmethod
    def get_user(payload):
        user = AccountService.get_account(payload.user_id)
        if not user:
            raise Unauthorized('登录已失效请重新登录')
        return user

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise Unauthorized(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise Unauthorized(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _(
                'Invalid token header. Token string should not contain invalid characters.')
            raise Unauthorized(msg)

        return self.authenticate_credentials(request, token)

    def authenticate_credentials(self, request, token):
        payload = getattr(request, 'payload', None)
        if payload and payload.user_id:
            user = self.get_user(payload)
        else:
            user = None
        return user, token

    def authenticate_header(self, request):
        return self.keyword
