from app01.models import *
import datetime, uuid
from app01.base_interface import code_generate


def obtain_class_info():
    """获取班级信息"""
    datalist = []
    class_queries = ClassInfo.objects.order_by('-year', 'code').all()
    for index, class_query in enumerate(class_queries):
        datalist.append({
            "rel_id": class_query.id,
            'id': index + 1,
            "name": class_query.name,
            "unique_code": class_query.unique_code,
            "code": class_query.code,
            "year": class_query.year,
        })
    return datalist


def add_class(class_name_list):
    """
    批量生成班级
    :param class_name_list: 班级名称列表
    :return: class_info_list
    """
    datalist = []
    # TODO 检查提交数据合法性
    year = str(datetime.datetime.now().year)
    for index, class_name in enumerate(class_name_list):
        code = code_generate.obtain_code(year, 1)
        class_query = ClassInfo.objects.create(name=class_name, unique_code=uuid.uuid4().hex, code=year + code,
                                               year=year)
        datalist.append({
            'rel_id': class_query.id,
            'id': index + 1,
            'name': class_query.name,
            'unique_code': class_query.unique_code,
            'code': class_query.code,
            'year': class_query.year
        })
    return datalist


def check_add_class():
    return


def student_obtain_class_info(class_unique_code):
    """学生获取班级同学信息"""
    datalist = []
    user_queries = UserInfo.objects.filter(class_unique_code=class_unique_code, user_type=3).all()
    id_index = 1
    for user_query in user_queries:
        datalist.append({
            'id': id_index,
            'rel_id': user_query.id,
            'name': user_query.username,
            'code': user_query.code,
        })
        id_index += 1
    return datalist


def get_class_info(class_unique_code):
    class_query = ClassInfo.objects.filter(unique_code=class_unique_code).first()
    teacher_code_queries = TeacherToClass.objects.filter(class_unique_code=class_query.unique_code).all()
    teacher_code_list = [teacher_code_query.teacher_unique_code for teacher_code_query in teacher_code_queries]
    teacher_queries = UserInfo.objects.filter(user_type=2, unique_code__in=teacher_code_list).all()
    teacher_info = []
    id_index = 1
    for teacher_query in teacher_queries:
        teacher_info.append({'id': id_index,
                             'name': teacher_query.username,
                             'code': teacher_query.code})
        id_index += 1
    data = {
        'teacher_info': teacher_info,
        'class_info': f'{class_query.name}-{class_query.year}'
    }
    return data
