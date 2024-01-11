from django.db import models
from users.models import User

# Create your models here.
NULLABLE = {'blank': 'True', 'null': 'True'}


class Course(models.Model):
    title_course = models.CharField(max_length=50, verbose_name='Название курса')
    image_course = models.ImageField(upload_to='course/', verbose_name='Картинка курса', **NULLABLE)
    description_course = models.TextField(verbose_name='Описание курса')

    author = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.title_course}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    title_lesson = models.CharField(max_length=50, verbose_name='Название урока')
    description_lesson = models.TextField(verbose_name='Описание урока')
    image_lesson = models.ImageField(upload_to='lesson/', verbose_name='Картинка урока', **NULLABLE)
    url_lesson = models.URLField(verbose_name='Ссылка на видео', **NULLABLE)
    url_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Ссылка на курс', **NULLABLE)

    author = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.title_lesson}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Subscription(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, **NULLABLE)
    course_subscription = models.ForeignKey(Course, verbose_name='курс в подписке', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} - {self.course_subscription}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
