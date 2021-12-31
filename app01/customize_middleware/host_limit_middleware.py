from django.utils.deprecation import MiddlewareMixin


class HostLimitMiddleware(MiddlewareMixin):
    """
    ip访问限制
    """

    def process_request(self, request):
        print(request.META.get('HTTP_X_FORWARDED_FOR'))


class DeviceCountMiddleware(MiddlewareMixin):
    """
    设备接口访问统计
    """

    def process_request(self, request):
        print(request.META.get('HTTP_X_FORWARDED_FOR'))
