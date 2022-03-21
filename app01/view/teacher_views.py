import json

from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt

from app01.admin_interface.user_operation import get_student_info, add_student, switch_student_class


def home(request):
    user = request.user
    return render(request, 'teacher/teacher_home.html', {'username': user.username})


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
