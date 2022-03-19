from app01.models import UserInfo
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class UserBackends(ModelBackend):
    # 自定义验证方法，通过邮箱或者用户名登陆
    def authenticate(self, request, username=None, password=None, **kwargs):
        username = username.strip()
        try:
            user = UserInfo.objects.get(code=username)
            if not user:
                user = UserInfo.objects.get(username=username)
            if not user:
                user = UserInfo.objects.get(phone_number=username)
            if user.check_password(password):
                return user
        except Exception as e:
            return None
