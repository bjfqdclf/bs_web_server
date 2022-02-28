from app01.models import UserInfo
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class UserBackends(ModelBackend):
    # 自定义验证方法，通过邮箱或者用户名登陆
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserInfo.objects.get(Q(name=username) | Q(code=int(username)))
            if user.check_password(password):
                return user
        except Exception as e:
            return None
