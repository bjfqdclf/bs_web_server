from django.conf import settings
from django.forms import model_to_dict
from app01.base_interface.tencent_cloud_service import tencent_cloud_service
from app01.models import *


class ApprovalService:

    def get_approval_list(self, user):
        """
        获取审批列表
        - 获取本人下的学生
        :param user:
        :return:
        """
        if user.user_type == 2:  # 教师获取该班级下的所有学生审批
            class_queries = TeacherToClass.objects.filter(teacher_unique_code=user.unique_code).all()
            class_unique_code = [class_query.class_unique_code for class_query in class_queries]
            class_info_queries = ClassInfo.objects.filter(unique_code__in=class_unique_code).all()
            class_info_map = {class_info_query.unique_code: f'{class_info_query.name}-{class_info_query.year}' for
                              class_info_query in class_info_queries}
            user_queries = UserInfo.objects.filter(class_unique_code__in=class_unique_code).all()
            user_map = {user_query.unique_code: {'username': user_query.username,
                                                 'code': user_query.code,
                                                 'class_name': class_info_map[user_query.class_unique_code]} for
                        user_query in user_queries}
            user_unique_code = [user_query.unique_code for user_query in user_queries]
            approval_info_queries = ApprovalInfo.objects.filter(user_unique_code__in=user_unique_code,
                                                                is_pass=False).all()
            datalist = []
            for approval_info_query in approval_info_queries:
                approval_info = model_to_dict(approval_info_query)
                approval_info['user_info'] = user_map[approval_info_query.user_unique_code]
                gen_time = approval_info['gen_time']
                approval_info[
                    'gen_time'] = f'{gen_time.year}-{gen_time.month} {gen_time.hour}:{gen_time.minute}:{gen_time.second}'
                datalist.append(approval_info)
            return datalist

    def get_a_approval_info(self, approval_unique_code):
        approval_query = ApprovalInfo.objects.filter(unique_code=approval_unique_code).first()
        data = model_to_dict(approval_query)
        user_query = UserInfo.objects.filter(unique_code=approval_query.user_unique_code).first()
        class_query = ClassInfo.objects.filter(unique_code=user_query.class_unique_code).first()
        gen_time = data['gen_time']
        data['gen_time'] = f'{gen_time.year}-{gen_time.month} {gen_time.hour}:{gen_time.minute}:{gen_time.second}'
        data['user_info'] = f'{user_query.username}-{user_query.code}'
        data['class_name'] = f'{class_query.name}-{class_query.code}'
        if approval_query.approval_type == 1:
            photo_query = UserPhoto.objects.filter(user_unique_code=approval_query.user_unique_code,
                                                   is_valid=False).first()
            data['img_unique_code'] = photo_query.unique_code
        else:
            data['img_unique_code'] = 'none'
        return data

    def pass_approval(self, approval_unique_code):
        """
        审核通过：
            - 需判断该条信息是否审核过，防止两个用户同时操作
        :param approval_unique_code:
        :return:
        """
        approval_query = ApprovalInfo.objects.filter(unique_code=approval_unique_code).first()
        if approval_query.is_pass:
            return '该审核记录已完成审核'
        else:
            if approval_query.approval_type == 1:
                UserPhoto.objects.filter(user_unique_code=approval_query.user_unique_code, is_valid=False).update(
                    is_valid=True)
                user_query = UserInfo.objects.filter(unique_code=approval_query.user_unique_code).first()
                person_exist = tencent_cloud_service.check_person_exist(user_query.code)
                if person_exist:
                    tencent_cloud_service.delete_face(user_query.code)
                user_info = {
                    "PersonName": user_query.username,
                    "PersonId": user_query.code,
                }
                picture_unique_code = UserPhoto.objects.filter(user_unique_code=approval_query.user_unique_code
                                                               , is_valid=True).first().unique_code
                img_dir = f'{settings.BASE_DIR}/static/upload_img/{picture_unique_code}.jpg'
                tencent_cloud_service.add_face(user_info, img_dir)
                ApprovalInfo.objects.filter(unique_code=approval_unique_code).update(is_pass=True)
                return '审核已通过'
            if approval_query.approval_type == 2:
                UserInfo.objects.filter(unique_code=approval_query.user_unique_code).update(can_edit_info=True)
                ApprovalInfo.objects.filter(unique_code=approval_unique_code).update(is_pass=True)
                return '审核已通过'


approval_service = ApprovalService()
