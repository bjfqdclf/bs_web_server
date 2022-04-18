from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from app01.base_interface.general_functions import edit_password
import json
from app01.models import *
from app01.admin_interface.class_interface import obtain_class_info, add_class
from app01.admin_interface.user_operation import get_teacher_info, add_teacher
from app01.base_interface.device_service import device_service


def home(request):
    user = request.user
    device_info = device_service.get_all_device_info()
    device_list = []
    index = 1
    for code, device in device_info.items():
        is_used = '是' if device['is_used'] else '否'
        device_list.append({
            'id': index,
            'code': code,
            'addr': device['address_desc'],
            'is_used': is_used
        })
        index += 1
    return render(request, 'admin/admin_home.html', {'username': user.username, 'device_list': device_list})


@csrf_exempt
def add_device_ajax(request):
    if request.method == 'POST':
        data = request.POST.dict()
        device_info = {}
        address_desc = data['address_desc']
        address_desc = address_desc.strip()
        if len(address_desc) >= 32:
            message = '设备地址描述太长！'
        elif len(address_desc) == 0:
            message = '描述不可为空'
        else:
            message, code = device_service.add_device(address_desc)
            count = device_service.count_device()
            device_info['addr'] = address_desc
            device_info['code'] = code
            device_info['is_used'] = '是'
            device_info['id'] = count
        data = {'status': 'success',
                'message': message,
                'device_info': device_info}
        return HttpResponse(json.dumps(data))


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
        name_list = []
        for value in new_data:
            if not value['name']:
                data = {'status': 'err',
                        'message': '班级名称不可为空！'}
                return HttpResponse(json.dumps(data))
            name_list.append(value['name'])
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


def teacher_manage(request):
    user = request.user
    teacher_info = get_teacher_info()
    class_list = obtain_class_info()
    select_class_info = [{'name': f'{class_value["name"]}-{class_value["year"]}',
                          'unique_code': class_value["unique_code"]} for class_value in class_list]
    return render(request, 'admin/admin_teacher_manage.html', {'username': user.username,
                                                               'teacher_list': teacher_info,
                                                               'class_list': select_class_info})


@csrf_exempt
def add_teacher_ajax(request):
    if request.method == 'POST':
        data = request.POST.dict()
        name = data['name']
        phone_number = data['phone_num']
        class_list = eval(data['select'])
        add_teacher(name, class_list, phone_number)
        data = {'status': 'success'}
        return HttpResponse(json.dumps(data))


@csrf_exempt
def get_teacher_class_ajax(request):
    if request.method == 'POST':
        datalist = []
        teacher_unique_code = request.POST.dict()['teacher_unique_code']
        teacher_id = request.POST.dict()['teacher_id']
        queries = TeacherToClass.objects.filter(teacher_unique_code=teacher_unique_code).all()
        for query in queries:
            class_query = ClassInfo.objects.filter(unique_code=query.class_unique_code).first()
            datalist.append(f'{class_query.name}-{class_query.year}')
        teacher_name = UserInfo.objects.filter(code=teacher_id).first().username
        data = {'status': 'success', 'class_list': datalist, 'username': teacher_name}
        return HttpResponse(json.dumps(data))


def edit_passwd(request):
    user = request.user
    return render(request, 'admin/admin_edit_passwd.html', {'username': user.username, 'code': user.code})
