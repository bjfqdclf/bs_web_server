from django.db import models
from django.contrib.auth.models import AbstractUser


class ClassInfo(models.Model):
    """班级"""
    uid = models.AutoField(primary_key=True)
    code = models.IntegerField()
    year = models.IntegerField()
    name = models.CharField(max_length=32, null=True)


class UserInfo(AbstractUser):
    code = models.IntegerField()
    name = models.CharField(max_length=32)
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


# 操作记录表
class DailyDataRecord(models.Model):
    type_code = models.IntegerField()  # 操作类型
    result_code = models.IntegerField(null=True)  # 操作结果状态码
    operation_user = models.IntegerField(null=True)  # 操作人员uid
    operation_msg = models.TextField(null=True)  # 操作具体信息
    time = models.DateTimeField()  # 操作时间


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
    data = models.DateTimeField(null=True)  # 移入时间

    # 外键
    user = models.ForeignKey(to='UserInfo', on_delete=models.CASCADE)
