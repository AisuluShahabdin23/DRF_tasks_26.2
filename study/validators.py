from rest_framework.serializers import ValidationError


class UrlValidator:
    """ Проверка на отсутствие в материалах ссылок на сторонние ресурсы (кроме youtube.com) """
    def __init__(self, field):
        self.field = field

    def __call__(self, url):
        temp_url = dict(url).get(self.field)
        if temp_url is not None and 'youtube.com' not in temp_url:
            raise ValidationError('Ссылка не может использоваться')
