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
