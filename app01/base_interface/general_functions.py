from django.contrib import auth
from app01.models import *
from app01.base_interface.code_generate import digit_completion
import uuid
from django.conf import settings
from app01.base_interface.tencent_cloud_service import tencent_cloud_service

def edit_password(data, user):
    old_password = data['old_password']
    new_password = data['new_password']
    re_password = data['re_password']
    old_user = auth.authenticate(username=user.code, password=old_password)
    if old_user is None:
        return {'status': 'false', 'message':'密码不正确'}
    if new_password != re_password:
        return {'status': 'false', 'message': '两次输入密码不一致'}
    old_user.set_password(new_password)
    old_user.save()
    return {'status': 'success', 'message': '密码修改成功'}


def get_user_type(user):
    if user == 1:
        user_type = 'admin'
    elif user == 2:
        user_type = 'teacher'
    else:
        user_type = 'student'
    return user_type


def up_load_img(img_data, user):
    user_photo = UserPhoto.objects.filter(user_unique_code=user.unique_code).delete()    # 删除已存在照片
    if user_photo:
        tencent_cloud_service.delete_face(user.unique_code)
    picture_unique_code = uuid.uuid4().hex
    file_path = f'{settings.BASE_DIR}/static/upload_img/{picture_unique_code}.jpg'
    with open(file_path, mode='wb+') as file_obj:
        for chunk in img_data.chunks():
            file_obj.write(chunk)
    UserPhoto.objects.create(unique_code=picture_unique_code, user_unique_code=user.unique_code)
    UserInfo.objects.filter(unique_code=user.unique_code).update(can_edit_info=False)
    return file_path


def get_picture_img(user_unique_code):
    img_query = UserPhoto.objects.filter(user_unique_code=user_unique_code).first()
    if img_query:
        img_unique_code = img_query.unique_code
        img_path = f'/static/upload_img/{img_unique_code}.jpg'
        is_valid = img_query.is_valid
    else:
        is_valid = False
        img_path = 'http://www.sucainiu.com/themes/index/images/headImg/no.png'
    return img_path, is_valid


def send_approval_info(user_unique_code, title, messages, approval_type=1):
    """
    发起审批
    :param approval_type: 审批类型，默认为照片审批
    :param user_unique_code: 被审批人
    :param title: 审批标题
    :param messages: 审批信息
    :return:
    """
    unique_code = uuid.uuid4().hex
    ApprovalInfo.objects.create(unique_code=unique_code,
                                user_unique_code=user_unique_code,
                                title=title, message=messages,
                                approval_type=approval_type)
