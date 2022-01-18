from django.db import models
from django.contrib.auth.models import AbstractUser
import django.utils.timezone as timezone


class ClassInfo(models.Model):
    """班级"""
    uid = models.AutoField(primary_key=True)
    code = models.IntegerField()  # 班级代码（1-999）
    year = models.IntegerField()  # 创建年份（2021）
    name = models.CharField(max_length=32, null=True)  # 名称


class UserInfo(AbstractUser):
    code = models.IntegerField()  # 工号/学号(2021001001)
    name = models.CharField(max_length=32)  # 姓名
    user_type = models.IntegerField()  # 1 管理员    2 老师    3 学生
    phone_number = models.IntegerField(null=True)

    # 外键
    class_info = models.ForeignKey(to='ClassInfo', null=True, on_delete=models.DO_NOTHING)


class TeacherToCass(models.Model):
    teacher_id = models.IntegerField()
    class_id = models.IntegerField()


class FaceImg(models.Model):
    """
    人脸照片
    一个人可以存入多张人脸图像
    """
    img = models.ImageField(height_field=500, width_field=500, null=True)
    is_active = models.BooleanField(default=True)  # 是否启用

    # 外键
    user = models.ForeignKey(to='UserInfo', on_delete=models.CASCADE)


class Massage(models.Model):
    """
    外部设备通知
    """
    type = models.IntegerField()  # 通知类型
    token = models.TextField(null=True)  # 通知识别码
    is_active = models.BooleanField(default=True)  # 是否启用

    # 外键
    user = models.ForeignKey(to='UserInfo', on_delete=models.CASCADE)


# 人脸识别记录表
class DailyFaceRecord(models.Model):
    person_name = models.CharField(max_length=32)
    person_id = models.IntegerField()
    temp = models.FloatField()
    time = models.DateTimeField('记录时间', auto_now=True)
    device_id = models.IntegerField()


class HistoryFaceRecord(models.Model):
    person_name = models.CharField(max_length=32)
    person_id = models.IntegerField()
    temp = models.FloatField()
    time = models.DateTimeField()
    device_id = models.IntegerField()


# 操作记录表
class DailyDataRecord(models.Model):
    type_code = models.IntegerField()  # 操作类型
    result_code = models.IntegerField(null=True)  # 操作结果状态码
    operation_user = models.IntegerField(null=True)  # 操作人员uid
    operation_msg = models.TextField(null=True)  # 操作具体信息
    time = models.DateTimeField('操作时间', auto_now=True)


class HistoryDataRecord(models.Model):
    type_code = models.IntegerField()  # 操作类型
    result_code = models.IntegerField(null=True)  # 操作结果状态码
    operation_user = models.IntegerField(null=True)  # 操作人员uid
    operation_msg = models.TextField(null=True)  # 操作具体信息
    time = models.DateTimeField()  # 操作时间


# web消息通知
class WebSysMassage(models.Model):
    type = models.IntegerField(null=True)  # 通知类型
    text = models.TextField(null=True)  # 通知内容
    status_code = models.IntegerField()  # 状态

    # 外键
    user = models.ForeignKey(to='UserInfo', on_delete=models.CASCADE)


class HistoryWebSysMassage(models.Model):
    """
    已完成通知
    """
    type = models.IntegerField()  # 通知类型
    text = models.TextField(null=True)  # 通知内容
    status_code = models.IntegerField()  # 状态
    data = models.DateTimeField('移入时间', auto_now=True, null=True)

    # 外键
    user = models.ForeignKey(to='UserInfo', on_delete=models.CASCADE)
