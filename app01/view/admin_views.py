from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from app01.base_interface.general_functions import edit_password
import json
from app01.models import *
from app01.admin_interface.class_interface import obtain_class_info


def home(request):
    user = request.user
    return render(request, 'admin/admin_home.html', {'username': user.username})


def add_user(request):
    user = request.user
    return render(request, 'admin/admin_add_teacher.html', {'username': user.username})


def class_manage(request):
    user = request.user
    class_list = obtain_class_info()
    return render(request, 'admin/admin_class_manage.html', {'username': user.username, 'class_list': class_list})


def edit_passwd(request):
    user = request.user
    return render(request, 'admin/admin_edit_passwd.html', {'username': user.username, 'code': user.code})

