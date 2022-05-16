# 1 概况

## 1.1 运行环境

- 服务器环境 Ubuntu 20.04 LTS 云服务器
- python3.8.10
- 云数据库 兼容mysql 5.7

# 2 基础配置

## 2.1 文件目录设置

- web_sys
    - app01
        - admin_interface
        - student_interface
        - teacher_interface
        - interface
        - migrations
        - customiz_middleware
        - view
            - public_views
            - admin_views
            - student_views
            - teacher_views
            - code_views
        - admin.py
        - models.py
        - apps.py
    - static
        - css
        - js
        - img
    - templates
        - admin
        - teacher
        - student
        - err_codes
    - web_sys
        - asgi.py
        - settings.py
        - urls.py
        - wsgi.py
    - conf_obtion.py
    - manage.py
    - web_sys.conf

## 2.2 配置

### 2.2.1 运行配置

> ../web_sys/web_sys/settigns.py
> 
- 将新增应用加入django环境变量

```
INSTALLED_APPS = [
'django.contrib.admin',
...
'app01',    # <<< 加入该行
]
```

- 新增中间件

```
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    ...
    'app01.customize_middleware.auth_middleware.AuthMiddleware',
    # <<< 加入该行
]
```

- 修改时区为中国

```
LANGUAGE_CODE = 'zh-hans'    # <<< 修改该行值
TIME_ZONE = 'Asia/Shanghai'    # <<< 修改该行值
```

- 增加静态文件夹

```
STATIC_URL = 'static/'    # <<< 加入该行
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)    # <<< 加入该行，并加入静态文件路径
```

- 修改用户登录方式

```
AUTH_USER_MODEL = "app01.UserInfo"    # 自定义用户表

AUTHENTICATION_BACKENDS = ['app01.auth_backend.user_backends.UserBackends', ]    # 自定义用户认证

LOGIN_URL = "/login/"    # 自定义用户登录URL
```

### 2.2.2 系统配置文件

```
[database]
db_engine = django.db.backends.mysql
db_name = web_sys_db
db_user = admin
db_password = 123456
db_addr = 127.0.0.1
db_port = 3306

[log]
file_dir = ../sys.log
out_put = True
file_level = INFO
stream_level = INFO
```

# 3 基础功能实现

## 3.1 第三方模块

## 3.2 自定义功能

### 3.2.1 自定义系统配置

### 3.2.2 自定义用户模块

### 3.2.2.1 自定义用户模型类

1. 用户类
    1. 新增自定义用户模型类（继承系统用户类AbstractUser）
    2. 在系统配置中注册自定义用户模型类

```
class UserInfo(AbstractUser):
    code = models.IntegerField(unique=True)  # 工号/学号(2021001001)
    name = models.CharField(max_length=32)  # 姓名
    user_type = models.IntegerField(unique=True)  # 1 管理员    2 老师    3 学生
    phone_number = models.IntegerField(null=True)
    REQUIRED_FIELDS = ['code', 'name', 'user_type']

    # 外键
    class_info = models.ForeignKey(to='ClassInfo', null=True, on_delete=models.DO_NOTHING)
```

> REQUIRED_FIELDS    系统创建管理员用户必填字段
> 
1. 用户登录中间件
    1. 用户登录中间件注册
    2. 用户登录中间件逻辑

```
class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        print(request.user.is_authenticated)
        white_list = settings.WHITE_LIST
        print('path:', request.path)
        if request.path in white_list:
            return None
        else:
            if request.user.is_authenticated:
                return None
            next_path = request.path
            return redirect(f'/login?next_path={next_path}')
```

> 系统无有效cookie，重定向至登录页面。登录认证通过后，可自动跳转至上一跳。
> 
1. 登录页面视图

```
def all_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        pwd = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=pwd)
        if user:
            auth.login(request, user)
            request.session.set_expiry(129600)  # 3天
            next_url = request.GET.get('next_path', '/login/')
            if next_url is "/login/":
                if user.user_type == 1:
                    return redirect('/admin/home')
                elif user.user_type == 2:
                    return redirect('/teacher/home')
                else:
                    return redirect('/student/home')
            return redirect(next_url)
        else:

            messages.error(request, '用户名或密码不正确')

            return render(request, 'index.html')
    if request.user.is_authenticated:
        user = request.user
        if user.user_type == 1:
            return redirect('/admin/home')
        elif user.user_type == 2:
            return redirect('/teacher/home')
        else:
            return redirect('/student/home')

    return render(request, 'index.html')
```

> - 非POST请求重定向至登录页面
> 

> - POST请求开始表单验证
> 

> - 验证成功，写入cookie，跳转至上一跳或角色对应主页
> 

> - 验证失败弹窗
> 
1. 自定义用户认证
    1. 系统配置自定义用户认证注册
    2. 新增自定义用户认证类（继承系统认证类ModelBackend）

```
class UserBackends(ModelBackend):
    # 自定义验证方法，通过邮箱或者用户名登陆
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserInfo.objects.get(Q(name=username) | Q(code=int(username)))
            if user.check_password(password):
                return user
        except Exception as e:
            return None
```

> 通过Q查询可自定义登录账号为用户名、邮箱、用户号码等字段
> 

> 使用password作为密码认证
> 

### 3.2.3 自定义路由限制

1. 中间件

```
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
```

> - 在白名单的URL所有用户均可访问
> 

> - 特定角色访问URL通过cookie的用户角色信息比对
> 

> - 用户访问URL无权限则返回401code
> 
1. 路由白名单

```
public_url = [
    '/login/',
    '/logout/',
    '/not_find/',
]

err_url = [
    '/404/',
    '/401/'
]

role_url_dict = {
    1: [  # admin_url
        '/admin/home',
    ],
    2: [  # teacher_url
        '/teacher/home',
    ],
    3: [  # student_url
        '/student/home',
    ]
}
```

> 将对应角色访问的URL添加至对应list
>



