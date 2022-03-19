from django.db import models
from django.contrib.auth.models import AbstractUser
import django.utils.timezone as timezone


class ClassInfo(models.Model):
    """班级"""
    name = models.CharField(max_length=32, help_text='班级名称')
    unique_code = models.CharField(max_length=256, help_text='班级唯一识别码')
    code = models.IntegerField(unique=True)
    year = models.IntegerField(help_text="班级年份(2021)")


class UserInfo(AbstractUser):
    code = models.CharField(unique=True, max_length=256, help_text='用户编号')  # 工号/学号(2021001001)
    unique_code = models.CharField(max_length=256, help_text='用户唯一识别码')
    user_type = models.IntegerField(unique=True, help_text='用户角色类型')  # 1-管理员、2-教师、3-学生
    phone_number = models.IntegerField(unique=True, null=True)

    class_unique_code = models.CharField(max_length=256, help_text='班级唯一识别码')
    REQUIRED_FIELDS = ['code', 'user_type']


class TeacherToClass(models.Model):
    teacher_unique_code = models.CharField(max_length=256, help_text='用户唯一识别码')
    class_unique_code = models.CharField(max_length=256, help_text='班级唯一识别码')


# 生成账号
class GenerateCode(models.Model):
    year = models.CharField(null=True, max_length=32, help_text='年份')
    code = models.CharField(max_length=32, help_text='编号')
    code_type = models.CharField(max_length=32, help_text='类型')     # 01-admin、02-教师、03-学生  1-班级


# 人脸识别记录表
class DailyFaceRecord(models.Model):
    person_name = models.CharField(max_length=32, help_text='用户名')
    person_code = models.IntegerField(help_text='用户code')
    temp = models.FloatField(help_text='记录温度')
    time = models.DateTimeField(help_text='记录时间', auto_now=True)
    device_code = models.CharField(max_length=32, help_text='设备编码')

# class FaceImg(models.Model):
#     """
#     人脸照片
#     一个人可以存入多张人脸图像
#     """
#     img = models.ImageField(height_field=500, width_field=500, null=True)
#     is_active = models.BooleanField(default=True)  # 是否启用
#
#     # 外键
#     user = models.ForeignKey(to='UserInfo', on_delete=models.CASCADE)
#
#
# class Massage(models.Model):
#     """
#     外部设备通知
#     """
#     type = models.IntegerField()  # 通知类型
#     token = models.TextField(null=True)  # 通知识别码
#     is_active = models.BooleanField(default=True)  # 是否启用
#
#     # 外键
#     user = models.ForeignKey(to='UserInfo', on_delete=models.CASCADE)
#
#


#
#
# class HistoryFaceRecord(models.Model):
#     person_name = models.CharField(max_length=32)
#     person_id = models.IntegerField()
#     temp = models.FloatField()
#     time = models.DateTimeField()
#     device_id = models.IntegerField()
#
#
# # 操作记录表
# class DailyDataRecord(models.Model):
#     type_code = models.IntegerField()  # 操作类型
#     result_code = models.IntegerField(null=True)  # 操作结果状态码
#     operation_user = models.IntegerField(null=True)  # 操作人员uid
#     operation_msg = models.TextField(null=True)  # 操作具体信息
#     time = models.DateTimeField('操作时间', auto_now=True)
#
#
# class HistoryDataRecord(models.Model):
#     type_code = models.IntegerField()  # 操作类型
#     result_code = models.IntegerField(null=True)  # 操作结果状态码
#     operation_user = models.IntegerField(null=True)  # 操作人员uid
#     operation_msg = models.TextField(null=True)  # 操作具体信息
#     time = models.DateTimeField()  # 操作时间
#
#
# # web消息通知
# class WebSysMassage(models.Model):
#     type = models.IntegerField(null=True)  # 通知类型
#     text = models.TextField(null=True)  # 通知内容
#     status_code = models.IntegerField()  # 状态
#
#     # 外键
#     user = models.ForeignKey(to='UserInfo', on_delete=models.CASCADE)
#
#
# class HistoryWebSysMassage(models.Model):
#     """
#     已完成通知
#     """
#     type = models.IntegerField()  # 通知类型
#     text = models.TextField(null=True)  # 通知内容
#     status_code = models.IntegerField()  # 状态
#     data = models.DateTimeField('移入时间', auto_now=True, null=True)
#
#     # 外键
#     user = models.ForeignKey(to='UserInfo', on_delete=models.CASCADE)
