from django.db.models import Count
from django.forms import model_to_dict

from app01.models import *


class MessageService:

    def get_message(self, user_unique_code, is_read):
        message_queries = MessageCenter.objects.filter(user_unique_code=user_unique_code,
                                                       is_read=is_read).all()
        datalist = []
        for message_query in message_queries:
            message_dict = model_to_dict(message_query)
            gen_time = message_dict['gen_time']
            message_dict['gen_time'] = f'{gen_time.year}-{gen_time.month} {gen_time.hour}:{gen_time.minute}:{gen_time.second}'
            datalist.append(message_dict)
        return datalist

    def get_message_puls(self,  user_unique_code):
        message_count = MessageCenter.objects.filter(user_unique_code=user_unique_code,
                                             is_read=False).aggregate(count=Count("id"))['count']
        message_queries = MessageCenter.objects.filter(user_unique_code=user_unique_code,
                                                       is_read=False).order_by("gen_time").all()
        if message_count == 0:
            return {'message_count': message_count,
                    'message_list': []}
        count = 0
        message_list = []
        for message_query in message_queries:
            if count > 3:
                break
            gen_time = message_query.gen_time
            message_list.append({
                'title': message_query.title,
                'message': message_query.message,
                'time': f'{gen_time.year}-{gen_time.month} {gen_time.hour}:{gen_time.minute}:{gen_time.second}'
            })
            count += 1
        return {'message_count': message_count,
                'message_list': message_list}



    def get_a_message(self, message_unique_code):
        message_query = MessageCenter.objects.filter(unique_code=message_unique_code).first()
        message_dict = model_to_dict(message_query)
        gen_time = message_dict['gen_time']
        message_dict['gen_time'] = f'{gen_time.year}-{gen_time.month} {gen_time.hour}:{gen_time.minute}:{gen_time.second}'
        return message_dict

    def read_a_message(self, message_unique_code):
        """一条消息已读"""
        message_query = MessageCenter.objects.filter(unique_code=message_unique_code).first()
        message_query.is_read = True
        message_query.save()
        return True

    def add_message(self, user_unique_code, data):
        MessageCenter.objects.create(**data)

    def create_new_user_message(self, user_unique_code):
        data = {
            'unique_code': uuid.uuid4().hex,
            'user_unique_code': user_unique_code,
            'level': 1,
            'type': 1,
            'title': '新用户须知',
            'message': '您的用户已创建，为了您的账户安全，请修改默认密码。点击忽略，以后不再提示。'
        }
        MessageCenter.objects.create(**data)

    def create_message(self, data):
        MessageCenter.objects.create(**data)

    def student_send_message(self, user, data):
        class_unique_code = user.class_unique_code
        teacher_queries = TeacherToClass.objects.filter(class_unique_code=class_unique_code).all()
        for teacher_query in teacher_queries:
            data['user_unique_code'] = teacher_query.teacher_unique_code
            data['unique_code'] = uuid.uuid4().hex
            MessageCenter.objects.create(**data)


message_service = MessageService()
