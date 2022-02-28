from django.utils.deprecation import MiddlewareMixin
from app01.customize_middleware.static import role_url
from django.shortcuts import redirect
from web_sys import settings


class RoleMiddleware(MiddlewareMixin):
    """
    用户权限url限制
    """

    def process_request(self, request):
        path = request.path
        user = request.user
        if path in role_url.err_url:
            return None
        if (not user.is_authenticated) and (path not in role_url.public_url):
            return redirect('/login/')
        if path not in role_url.public_url:
            user_type = user.user_type
            if path not in role_url.role_url_dict[user_type]:
                return redirect('/401/')
