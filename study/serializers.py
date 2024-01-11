from rest_framework import serializers

from study.models import Lesson, Course, Subscription
from study.validators import UrlValidator


class SubscriptionSerializer(serializers.ModelSerializer):
    """ Сериализатор модели подписки """
    class Meta:
        model = Subscription
        fields = '__all__'


class LessonCourseSerializer(serializers.ModelSerializer):
    """ Cериализатор для Course, который будет включать данные об уроках """
    class Meta:
        model = Lesson
        fields = ('pk', 'title_lesson',)


class CourseCreateSerializer(serializers.ModelSerializer):
    """ Сериализатор для создания Course"""
    class Meta:
        model = Course
        fields = ('title_course', 'description_course',)


class CourseSerializer(serializers.ModelSerializer):
    """ Сериализатор модели Course"""
    lessons_count = serializers.IntegerField(source='lesson_set.all.count', read_only=True)  # поле вывода количества уроков
    lessons = LessonCourseSerializer(source='lesson_set', read_only=True, many=True)  # поле вывода уроков
    course_subscription = serializers.SerializerMethodField()

    def get_course_subscription(self, obj):
        """ Метод вывода подписан пользователь на курс """
        return Subscription.objects.filter(course_subscription=obj, user=self.context['request'].user).exists()

    def get_lessons_count(self, instance):
        """ Метод вывода количества уроков """
        return instance.lesson_set.count()

    class Meta:
        model = Course
        fields = ('pk', 'title_course', 'image_course', 'description_course', 'lessons_count', 'lessons',
                  'course_subscription',)


class LessonSerializer(serializers.ModelSerializer):
    """ Сериализатор модели Lesson """
    class Meta:
        model = Lesson
        fields = '__all__'  # Вывод всех полей
        validators = [UrlValidator(field='url_lesson')]
