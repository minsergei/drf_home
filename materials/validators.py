from rest_framework.serializers import ValidationError
import re


def valid_link(value):
    reg = re.compile('^https://rutube.ru/')
    if not bool(reg.match(value)):
        raise ValidationError('Ссылка должны быть с rutube.ru')
