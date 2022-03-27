from app01.models import *
from app01.base_interface.general_functions import send_approval_info

class PhotoService:

    def check_can_initiate_approval(self, user):
        approval_info_query = ApprovalInfo.objects.filter(user_unique_code=user.unique_code,
                                                          is_pass=False).first()
        if approval_info_query:
            return False
        else:
            return True

    def initiate_photo_approval(self, user):
        approval_title = f'学生{user.username}请求权限'
        approval_messages = f'权限请求>>>:[{user.username}]-[{user.code}]-[请求开启上传照片权限]'
        send_approval_info(user.unique_code, approval_title, approval_messages, 2)


student_photo_service = PhotoService()
