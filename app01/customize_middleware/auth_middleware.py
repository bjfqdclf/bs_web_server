from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import authenticate,login
from django.shortcuts import redirect
from web_sys import settings


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        print(request.user.is_authenticated)
        if not request.user.is_authenticated:
            white_list = settings.WHITE_LIST
            print('path:', request.path)
            if request.path in white_list:
                return None
            else:
                next_path = request.path
                return redirect(f'/login?next_path={next_path}')
