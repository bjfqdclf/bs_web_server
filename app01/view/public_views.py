import uuid

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import auth, messages
from django.views.decorators.csrf import csrf_exempt
from app01.base_interface.general_functions import edit_password, get_user_type, up_load_img, send_approval_info
from app01.base_interface.message_center_service import message_service
import json


def all_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        pwd = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=pwd)
        if user:
            auth.login(request, user)
            request.session.set_expiry(129600)  # 3天
            next_url = request.GET.get('next_path', '/login/')
            if next_url == "/login/":
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


def logout(request):
    """退出账户"""
    request.session.flush()
    return render(request, 'index.html')


@csrf_exempt
def edit_passwd_ajax(request):
    user = request.user
    if request.method == 'POST':
        data = request.POST

        re_data = edit_password(data, user)
        status = re_data['status']
        if status == 'success':
            request.session.flush()
        return HttpResponse(json.dumps(re_data))


def message_center(request):
    user = request.user
    user_type = get_user_type(user.user_type)
    is_read_message_list = message_service.get_message(user.unique_code, True)
    not_read_message_list = message_service.get_message(user.unique_code, False)
    data = {
        'title': '今日新闻',
        'message': '美国部分地区已开始人口清除计划，MATE公司总裁扎克伯格将担任新一届美国总统，届时将由机器人掌控美国。'
    }
    # message_service.add_message(user.unique_code, data)
    return render(request, f'{user_type}/{user_type}_message_center.html',
                  {'username': user.username,
                   'is_read_message_list': is_read_message_list,
                   'not_read_message_list': not_read_message_list})


@csrf_exempt
def get_message_detail_ajax(request):
    if request.method == 'POST':
        message_unique_code = request.POST.dict()['message_unique_code']
        message_info = message_service.get_a_message(message_unique_code)
        re_data = {'status': 'success',
                   'message_info': message_info}
        return HttpResponse(json.dumps(re_data))


@csrf_exempt
def message_read_ajax(request):
    """消息已读"""
    if request.method == 'POST':
        message_unique_code = request.POST.dict()['message_unique_code']
        message_service.read_a_message(message_unique_code)
        re_data = {'status': 'success'}
        return HttpResponse(json.dumps(re_data))


@csrf_exempt
def upload_img_ajax(request):
    """上传图片"""
    user = request.user
    if request.method == 'POST':
        upload_img = request.FILES['image']
        file_path = up_load_img(upload_img, user)
        data = {
            'level': 1,
            'type': 1,
            'title': '新的审批',
            'message': f'照片审批>>>:[{user.username}]-[{user.code}]，请至审批页面进行审批'
        }
        message_service.student_send_message(user, data)
        approval_title = f'学生{user.username}照片审批'
        approval_messages = f'照片审批>>>:[{user.username}]-[{user.code}]'
        send_approval_info(user.unique_code, approval_title, approval_messages)
        return HttpResponse(json.dumps(file_path))


@csrf_exempt
def message_center_pupups_ajax(request):
    """消息弹窗通知"""
    user = request.user
    if request.method == 'POST':
        re_data = message_service.get_message_puls(user.unique_code)
        return HttpResponse(json.dumps(re_data))


def url_404(request):
    return render(request, 'ok')

