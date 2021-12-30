from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from web_sys import settings


class RoleMiddleware(MiddlewareMixin):

    def process_request(self, request):
        pass
    #     role_url_list = settings.ROLE_URL_LIST
    #     if request.path in role_url_list:
    #         user = request.user
    #         if user.is_authenticated:
    #             user_type = user.user_type
    #             if user_type == 1:  # admin
    #                 path = f'/admin{request.path}'
    #             elif user_type == 2:  # teacher
    #                 path = f'/teacher{request.path}'
    #             elif user_type == 3:  # student
    #                 path = f'/student{request.path}'
    #             else:
    #                 path = request.path
    #             return redirect(path)

