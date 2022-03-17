from app01.models import UserInfo, ClassInfo
from app01.base_interface import code_generate


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
