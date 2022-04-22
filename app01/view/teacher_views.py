import json

from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from app01.teacher_interface.approval_service import approval_service
from app01.admin_interface.user_operation import get_student_info, add_student, switch_student_class
from app01.view.public_views import punch_record


def home(request):
    user = request.user
    punch_record_list = punch_record(user)
    return render(request, 'teacher/teacher_home.html', {'username': user.username, 'punch_record_list' :punch_record_list})


def edit_passwd(request):
    user = request.user
    return render(request, 'teacher/teacher_edit_passwd.html', {'username': user.username, 'code': user.code})


def student_manage(request):
    user = request.user
    user_unique_code = user.unique_code
    student_info, class_info = get_student_info(user_unique_code)
    return render(request, 'teacher/teacher_student_manage.html',
                  {'username': user.username, 'student_info': student_info, 'class_info': class_info})


@csrf_exempt
def add_student_ajax(request):
    if request.method == 'POST':
        data = request.POST.dict()
        add_student(data['name'], data['select'], data['phone_num'])
        data = {'status': 'success'}
        return HttpResponse(json.dumps(data))


@csrf_exempt
def switch_student_class_ajax(request):
    if request.method == 'POST':
        data = request.POST.dict()
        switch_student_class(data['student_unique_code'], data['class_unique_code'])
        data = {'status': 'success'}
        return HttpResponse(json.dumps(data))


def cat_approval(request):
    user = request.user
    approval_info = approval_service.get_approval_list(user)
    return render(request, 'teacher/teacher_cat_approval.html', {'username': user.username,
                                                                 'approval_info': approval_info})


@csrf_exempt
def cat_a_approval_ajax(request):
    if request.method == 'POST':
        approval_unique_code = request.POST.dict()['unique_code']
        approval_info = approval_service.get_a_approval_info(approval_unique_code)
        img_path = f'/static/upload_img/{approval_info["img_unique_code"]}.jpg'
        data = {'status': 'success',
                'approval_type': approval_info['approval_type'],
                'approval_info': approval_info,
                'img_path': img_path}
        return HttpResponse(json.dumps(data))


@csrf_exempt
def pass_approval_ajax(request):
    if request.method == 'POST':
        is_pass = request.POST.dict()['pass']
        approval_unique_code = request.POST.dict()['unique_code']
        if is_pass == 'true':
            message = approval_service.pass_approval(approval_unique_code)
            data = {'status': 'success', 'message': message}
        else:
            message = approval_service.not_pass_approval(approval_unique_code)
            data = {'status': 'success', 'message': message}
        return HttpResponse(json.dumps(data))
