from app01.models import ClassInfo
import datetime


def create_class(name, code, year=None):
    year = year if year else datetime.datetime.now().year
    class_obj = ClassInfo.objects.create(
        year=year,
        name=name,
        code=code,
    )

    return True if class_obj else False
