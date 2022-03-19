from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from app01.base_interface.general_functions import edit_password
import json
from app01.models import *
from app01.admin_interface.class_interface import obtain_class_info, add_class


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


@csrf_exempt
def add_class_ajax(request):
    if request.method == 'POST':
        data = request.POST.dict()
        for key in data.keys():
            new_data = eval(key)
        name_list = [value['name'] for value in new_data]
        datalist = add_class(name_list)
        data = {'status': 'success',
                'datalist': datalist}
        return HttpResponse(json.dumps(data))


@csrf_exempt
def get_class_info_ajax(request):
    if request.method == 'POST':
        datalist = obtain_class_info()
        data = {'status': 'success'}
        return HttpResponse(json.dumps(data))


def edit_passwd(request):
    user = request.user
    return render(request, 'admin/admin_edit_passwd.html', {'username': user.username, 'code': user.code})
