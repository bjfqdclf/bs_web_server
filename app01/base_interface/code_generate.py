from app01.models import *
def digit_completion(num, bit_num):
    """
    补全数字位数并转为字符串
    :param num: 需要补全的数字
    :param bit_num: 补全后的位数
    :return:
    """
    num = str(num)
    num_now_len = len(num)
    add_bit_num = bit_num - num_now_len
    for i in range(add_bit_num):
        num = f'{0}{num}'
    return num


def obtain_code(year, code_type):
    """
    获取code
    :param year: 年份
    :param code_type: 类型
    :return: str
    """
    code_query = GenerateCode.objects.filter(year=year, code_type=code_type).order_by('code').first()
    if not code_query:
        GenerateCode.objects.create(year=year, code_type=code_type, code='2')
        code = 1
    else:
        code = int(code_query.code)
        code_query.code = str(code+1)
        code_query.save()

    if code_type == 4:
        return digit_completion(code, 5)
    return digit_completion(code, 3)
