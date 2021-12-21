from django.db import models


class Admin(models.Model):
    """管理员"""
    uid = models.AutoField(primary_key=True)
    code = models.IntegerField()
    name = models.CharField(max_length=32)
    password = models.TextField()
    phone_number = models.IntegerField(null=True)


class Teacher(models.Model):
    """老师"""
    uid = models.AutoField(primary_key=True)
    code = models.IntegerField()
    name = models.CharField(max_length=32)
    password = models.TextField()
    phone_number = models.IntegerField(null=True)

    # 外键


class Student(models.Model):
    """学生"""
    uid = models.AutoField(primary_key=True)
    code = models.IntegerField()
    name = models.CharField(max_length=32)
    password = models.TextField()
    phone_number = models.IntegerField(null=True)

    # 外键
    student = models.ForeignKey(to='Class', to_filed='uid')


class Class(models.Model):
    """班级"""
    uid = models.AutoField(primary_key=True)
    code = models.IntegerField()
    year = models.IntegerField()
    name = models.CharField(max_length=32, null=True)

    # 外键
    teacher = models.ForeignKey(to='Teacher', to_filed='uid')


class FaceImg(models.Model):
    """
    人脸照片
    一个人可以存入多张人脸图像
    """
    img = models.ImageField(height_field=500, width_field=500)
    is_active = models.BooleanField(default=True)  # 是否启用

    # 外键
    student = models.ForeignKey(to='Student', on_delete=models.CASCADE)
    teacher = models.ForeignKey(to='Teacher', on_delete=models.CASCADE)


class Masage(models.Model):
    """
    通知
    """
    type = models.IntegerField()  # 通知类型
    code = models.TextField(null=True)  # 通知识别码
    is_active = models.BooleanField(default=True)  # 是否启用

    # 外键
    admin = models.ForeignKey(to='Admin', on_delete=models.CASCADE)
    teacher = models.ForeignKey(to='Teacher', on_delete=models.CASCADE)


# 操作记录表
class DailyDataRecord(models.Model):
    type_code = models.IntegerField()  # 操作类型
    result_code = models.IntegerField()  # 操作结果状态码
    operation_user = models.IntegerField()  # 操作人员uid
    operation_msg = models.TextField()  # 操作具体信息
    time = models.CharField()  # 操作时间


class HistoryDataRecord(models.Model):
    type_code = models.IntegerField()  # 操作类型
    result_code = models.IntegerField()  # 操作结果状态码
    operation_user = models.IntegerField()  # 操作人员uid
    operation_msg = models.TextField()  # 操作具体信息
    time = models.DateTimeField()  # 操作时间
    data = models.DateTimeField()


# web消息通知
class WebSysMassage(models.Model):
    type = models.IntegerField()  # 通知类型
    text = models.TextField()  # 通知内容
    status_code = models.IntegerField()  # 状态

    # 外键
    teacher = models.ForeignKey(to='Teacher', on_delete=models.CASCADE)
    student = models.ForeignKey(to='Student', on_delete=models.CASCADE)
    admin = models.ForeignKey(to='Admin', on_delete=models.CASCADE)


class HistoryWebSysMassage(models.Model):
    """
    已完成通知
    """
    type = models.IntegerField()  # 通知类型
    text = models.TextField()  # 通知内容
    status_code = models.IntegerField()  # 状态
    data = models.DateTimeField()  # 移入时间

    # 外键
    teacher = models.ForeignKey(to='Teacher', on_delete=models.CASCADE)
    student = models.ForeignKey(to='Student', on_delete=models.CASCADE)
    admin = models.ForeignKey(to='Admin', on_delete=models.CASCADE)
