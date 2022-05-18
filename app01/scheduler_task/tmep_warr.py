from apscheduler.scheduler import Scheduler
import datetime
from app01.models import *
from app01.base_interface.log_server import LogServer
from app01.base_interface.message_center_service import MessageService
# 实例化
temp_scheduler_service = Scheduler()


# 每5分钟执行一次
@temp_scheduler_service.interval_schedule(seconds=300)
def scheduler_test():
    log = LogServer('温度检测定时任务')
    """
    测试-定时将随机数保存到redis中
    :return:
    """
    try:
        now_time = datetime.datetime.now()
        start_time = now_time + datetime.timedelta(minutes=-5)
        face_record_queries = DailyFaceRecord.objects.filter(time__range=(start_time, now_time))
        for face_record_query in face_record_queries:
            if face_record_query.temp > 41:
                person_code = face_record_query.person_code
                user_info = UserInfo.objects.filter(code=person_code).first()
                class_unique_code = user_info.class_unique_code
                teacher_queries = TeacherToClass.objects.filter(class_unique_code=class_unique_code)
                for teacher_query in teacher_queries:
                    data = {
                        'unique_code': uuid.uuid4().hex,
                        'user_unique_code': teacher_query.teacher_unique_code,
                        'level': 1,
                        'type': 1,
                        'title': '温度异常通知',
                        'message': f'学生{user_info.username}-{user_info.code}的温度异常，温度为{face_record_query.temp}。'
                    }
                    MessageService.create_message(data)

    except Exception as e:
        log.error(e)
