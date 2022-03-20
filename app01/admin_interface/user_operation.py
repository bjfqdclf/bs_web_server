from app01.models import *
from app01.base_interface import code_generate
import datetime, uuid


def creat_student():
    user = UserInfo.objects.create_user(username='ligoudan', password='1', name='李狗蛋', code='18', user_type=1)
    return user


def students_code_generate(class_id, num):
    """
    学号生成
    class_year+class_code+num
    2021        001       001
    :return:
    """
    class_obj = ClassInfo.objects.filter(uid=class_id).first()
    code = int(
        f'{code_generate.digit_completion(class_obj.year, 4)}{code_generate.digit_completion(class_obj.code, 3)}{code_generate.digit_completion(num, 3)}')
    return code


def get_teacher_info():
    teacher_queries = UserInfo.objects.filter(user_type=2).all()
    datalist = []
    index = 1
    for teacher_query in teacher_queries:
        datalist.append({'id': index,
                         'rel_id': teacher_query.id,
                         'name': teacher_query.username,
                         'code': teacher_query.code,
                         'phone_num': teacher_query.phone_number,
                         'unique_code': teacher_query.unique_code})
        index += 1
    return datalist


def add_teacher(name, class_list, phone_num=None):
    """
    添加老师
    :param name:
    :param class_list:
    :param phone_num:
    :return:
    """
    year = str(datetime.datetime.now().year)
    code = code_generate.obtain_code(year, 2)
    rel_code = year + code + '2'
    unique_code = uuid.uuid4().hex
    user_query = UserInfo.objects.create(username=name, code=rel_code,
                                         unique_code=unique_code,
                                         phone_number=phone_num, user_type=2)
    user_query.set_password('1')
    for class_unique_code in class_list:
        TeacherToClass.objects.create(class_unique_code=class_unique_code, teacher_unique_code=user_query.unique_code)
    return True
