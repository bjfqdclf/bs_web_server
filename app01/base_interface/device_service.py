from app01.models import DeviceRegister


class DeviceService:

    def get_all_used_device_info(self):
        device_info = {}
        device_queries = DeviceRegister.objects.filter(is_used=True).all()
        for device_query in device_queries:
            device_info[device_query.code] = {'address_desc': device_query.address_desc}
        return device_info


device_service = DeviceService()
