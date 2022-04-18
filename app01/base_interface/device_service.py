import datetime

from django.db.models import Count

from app01.base_interface import code_generate
from app01.models import DeviceRegister


class DeviceService:

    def get_all_device_info(self):
        device_info = {}
        device_queries = DeviceRegister.objects.all()
        for device_query in device_queries:
            device_info[device_query.code] = {'address_desc': device_query.address_desc,
                                              'is_used': device_query.is_used}
        return device_info

    def add_device(self, address_desc):
        year = str(datetime.datetime.now().year)
        code = code_generate.obtain_code(year, 4)
        rel_code = year + code
        DeviceRegister.objects.create(address_desc=address_desc,
                                      code=rel_code)
        return '添加设备成功！', rel_code

    def count_device(self):
        count = DeviceRegister.objects.aggregate(count=Count("id"))
        return count['count'] + 1


device_service = DeviceService()
