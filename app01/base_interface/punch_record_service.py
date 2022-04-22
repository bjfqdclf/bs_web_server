from copy import deepcopy

from app01.models import *


class PunchRecordService:

    def get_teacher_students(self, teacher_unique_code, user_code_list):
        class_queries = TeacherToClass.objects.filter(teacher_unique_code=teacher_unique_code).all()
        class_unique_codes = [class_query.class_unique_code for class_query in class_queries]
        user_queries = UserInfo.objects.filter(class_unique_code__in=class_unique_codes, user_type=3).all()
        user_code_list.extend([user_query.code for user_query in user_queries])

    def get_punch_record(self, user_code_list):
        face_record_queries = DailyFaceRecord.objects.filter(person_code__in=user_code_list).order_by("time").all()
        user_queries = UserInfo.objects.filter(code__in=user_code_list).all()
        class_unique_codes = [user_query.class_unique_code for user_query in user_queries]
        class_queries = ClassInfo.objects.filter(unique_code__in=class_unique_codes).all()
        class_map = {class_query.unique_code: f'{class_query.year}-{class_query.name}' for class_query in class_queries}
        user_map = {user_query.code: {'name': user_query.username,
                                      'code':  user_query.code,
                                      'class': class_map[user_query.class_unique_code],}
                    for user_query in user_queries}
        device_queries = DeviceRegister.objects.filter(is_used=True).all()
        device_address_map = {device_query.code: device_query.address_desc for device_query in device_queries}
        punch_record_list = []
        for face_record_query in face_record_queries:
            if str(face_record_query.person_code) in user_map.keys() and str(face_record_query.device_code) in device_address_map.keys():
                gen_time = face_record_query.time
                punch_record = deepcopy(user_map[str(face_record_query.person_code)])
                punch_record['temp'] = face_record_query.temp
                punch_record['time'] = f'{gen_time.year}-{gen_time.month} {gen_time.hour}:{gen_time.minute}:{gen_time.second}'
                punch_record['address_dec'] = device_address_map[str(face_record_query.device_code)]
                punch_record_list.append(punch_record)
        return punch_record_list


punch_record_service = PunchRecordService()
