from django.shortcuts import render, HttpResponse, redirect
from app01.admin_interface.class_interface import student_obtain_class_info, get_class_info


def home(request):
    user = request.user
    return render(request, 'student/student_home.html', {'username': user.username})


def edit_passwd(request):
    user = request.user
    return render(request, 'student/student_edit_passwd.html', {'username': user.username, 'code': user.code})


def cat_class(request):
    user = request.user
    user_info = student_obtain_class_info(user.class_unique_code)
    class_info = get_class_info(user.class_unique_code)
    return render(request, 'student/student_cat_class.html',
                  {'username': user.username, 'user_info': user_info, 'class_info': class_info})
