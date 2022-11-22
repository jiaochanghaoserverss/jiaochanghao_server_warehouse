# -*- coding: utf-8 -*-


from rest_framework.permissions import IsAuthenticated as SysAuth

from common import const
from common.exceptions import Unauthorized


class IsAuthenticated(SysAuth):
    def has_permission(self, request, view):
        return bool(request.user and request.user.id)


class RolesAuthenticated(SysAuth):
    def has_permission(self, request, view):
        # 暂时只支持viewSet角色校验
        if not getattr(view, 'action_roles_authenticated', None) and not getattr(view, 'action', None):
            return True
        # 没有配置默认角色可以访问
        if not view.action_roles_authenticated:
            return True
        action_roles = view.action_roles_authenticated
        roles = action_roles.get(view.action) if action_roles.get(view.action, None) else action_roles.get('default')
        if not roles:
            return True

        # 特殊角色
        if const.DefaultRole.ALL in roles:
            return True

        # 有指定角色才可以访问
        user_roles = [role.name for role in request.user.roles()]
        for r in roles:
            if r in user_roles:
                return True
        return False


class IsAdminAuthenticated(SysAuth):
    def has_permission(self, request, view):
        try:
            request.user.is_admin
        except:
            raise Unauthorized('请先登录')
        return bool(request.user and request.user.is_admin)
