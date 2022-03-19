from app01.models import ClassInfo
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
    year = str(datetime.datetime.now().year)
    for index, class_name in enumerate(class_name_list):
        code = code_generate.obtain_code(year, 1)
        class_query = ClassInfo.objects.create(name=class_name, unique_code=uuid.uuid4().hex, code=year+code, year=year)
        datalist.append({
            'rel_id': class_query.id,
            'id': index + 1,
            'name': class_query.name,
            'unique_code': class_query.unique_code,
            'code': class_query.code,
            'year': class_query.year
        })
    return datalist

