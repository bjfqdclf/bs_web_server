import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse, redirect
from app01.admin_interface.class_interface import student_obtain_class_info, get_class_info
from app01.base_interface.general_functions import get_picture_img
from app01.student_interface.photo_service import student_photo_service


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


def edit_photo_manage(request):
    user = request.user
    img_path, is_valid = get_picture_img(user.unique_code)
    return render(request, 'student/student_edit_photo.html', {'username': user.username,
                                                               'img_path': img_path,
                                                               'is_valid': is_valid,
                                                               'can_edit_info': user.can_edit_info})


@csrf_exempt
def initiate_approval_ajax(request):
    user = request.user
    can_initiate_approval = student_photo_service.check_can_initiate_approval(user)
    if not can_initiate_approval:
        data = {'status': 'False', 'message': '已存在审批，等待审批通过'}
    else:
        student_photo_service.initiate_photo_approval(user)
        data = {'status': 'success', 'message': '已发起审批，等待审批通过'}
    return HttpResponse(json.dumps(data))
