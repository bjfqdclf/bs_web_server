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
    user_query.save()
    for class_unique_code in class_list:
        TeacherToClass.objects.create(class_unique_code=class_unique_code, teacher_unique_code=user_query.unique_code)
    return True


def get_student_info(teacher_unique_code):
    class_queries = TeacherToClass.objects.filter(teacher_unique_code=teacher_unique_code).all()
    if not class_queries:
        class_unique_code_list = []
    else:
        class_unique_code_list = [class_query.class_unique_code for class_query in class_queries]
    class_queries = ClassInfo.objects.filter(unique_code__in=class_unique_code_list)
    class_list = [{'name': f'{class_query.name}-{class_query.year}',
                   'unique_code': class_query.unique_code} for class_query in class_queries]
    class_map = {class_query.unique_code: f'{class_query.name}-{class_query.year}' for class_query in class_queries}
    student_queries = (UserInfo.objects
                       .filter(user_type=3,
                               class_unique_code__in=class_unique_code_list)
                       .order_by('class_unique_code', 'code').all())
    student_info_list = []
    id_index = 1
    for student_query in student_queries:
        student_info_list.append({'id': id_index,
                                  'rel_id': student_query.id,
                                  'name': student_query.username,
                                  'code': student_query.code,
                                  'class_name': class_map[student_query.class_unique_code],
                                  'name_code': f'{student_query.username}-{student_query.code}',
                                  'phone_num': student_query.phone_number,
                                  'unique_code': student_query.unique_code})
        id_index += 1
    return student_info_list, class_list


def add_student(name, class_unique_code, phone_num=None):
    """
    添加学生
    :param name:
    :param class_unique_code:
    :param phone_num:
    :return:
    """
    year = str(datetime.datetime.now().year)
    code = code_generate.obtain_code(year, 3)
    rel_code = year + code + '3'
    unique_code = uuid.uuid4().hex
    if not phone_num:
        user_query = UserInfo.objects.create(username=name, code=rel_code,
                                             unique_code=unique_code, class_unique_code=class_unique_code,
                                             user_type=3)
    else:
        user_query = UserInfo.objects.create(username=name, code=rel_code,
                                             unique_code=unique_code, class_unique_code=class_unique_code,
                                             phone_number=phone_num, user_type=3)
    user_query.set_password('1')
    user_query.save()
    return True


def switch_student_class(student_unique_code, class_unique_code):
    """
    切换学生班级
    :param student_unique_code:
    :param class_unique_code:
    :return:
    """
    student = UserInfo.objects.filter(unique_code=student_unique_code).first()
    student.class_unique_code = class_unique_code
    student.save()
    return True
