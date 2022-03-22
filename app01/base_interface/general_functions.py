from django.contrib import auth
from app01.models import *
from app01.base_interface.code_generate import digit_completion


def edit_password(data, user):
    old_password = data['old_password']
    new_password = data['new_password']
    re_password = data['re_password']
    old_user = auth.authenticate(username=user.code, password=old_password)
    if old_user is None:
        return {'status': 'false', 'message':'密码不正确'}
    if new_password != re_password:
        return {'status': 'false', 'message': '两次输入密码不一致'}
    old_user.set_password(new_password)
    old_user.save()
    return {'status': 'success', 'message': '密码修改成功'}


def get_user_type(user):
    if user == 1:
        user_type = 'admin'
    elif user == 2:
        user_type = 'teacher'
    else:
        user_type = 'student'
    return user_type

