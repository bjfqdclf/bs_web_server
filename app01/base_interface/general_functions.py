from django.contrib import auth


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

