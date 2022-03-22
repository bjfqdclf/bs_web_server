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
            'user_unique_code': user_unique_code,
            'level': 1,
            'type': 1,
            'title': '新用户须知',
            'message': '您的用户已创建，为了您的账户安全，请修改默认密码。点击忽略，以后不再提示。'
        }
        MessageCenter.objects.create(**data)


message_service = MessageService()
