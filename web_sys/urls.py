"""web_sys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from app01.view import public_views, admin_views, teacher_views, student_views

urlpatterns = [
    # 系统public页面
    path('', public_views.all_login),
    path('login/', public_views.all_login),
    path('logout/', public_views.logout),
    path('not_find/', public_views.url_404),
    path('edit_passwd_ajax/', public_views.edit_passwd_ajax),
    path('get_message_detail_ajax/', public_views.get_message_detail_ajax),
    path('message_read_ajax/', public_views.message_read_ajax),


    # 管理员页面
    path('admin/home/', admin_views.home),
    path('admin/add/user/', admin_views.add_user),
    path('admin/edit_passwd/', admin_views.edit_passwd),
    path('admin/class_manage/', admin_views.class_manage),
    path('admin/add_class_ajax/', admin_views.add_class_ajax),
    path('admin/teacher_manage/', admin_views.teacher_manage),
    path('admin/add_teacher_ajax/', admin_views.add_teacher_ajax),
    path('admin/get_teacher_class_ajax/', admin_views.get_teacher_class_ajax),
    path('admin/message_center/', public_views.message_center),


    # 教师页面
    path('teacher/home/', teacher_views.home),
    path('teacher/edit_passwd/', teacher_views.edit_passwd),
    path("teacher/student_manage/", teacher_views.student_manage),
    path('teacher/add_student_ajax/', teacher_views.add_student_ajax),
    path('teacher/switch_student_class_ajax/', teacher_views.switch_student_class_ajax),
    path('teacher/message_center/', public_views.message_center),

    # 学生页面
    path('student/home/', student_views.home),
    path('student/edit_passwd/', student_views.edit_passwd),
    path('student/cat_class/', student_views.cat_class),
    path('student/message_center/', public_views.message_center),

]
