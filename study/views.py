from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from study.models import Course, Lesson, Subscription
from study.paginations import LessonPaginator
from study.permissions import IsModeratorOrReadOnly, IsCourseOwner, IsCourseOrLessonOwner
from study.serializers import CourseSerializer, LessonSerializer, CourseCreateSerializer, SubscriptionSerializer
from users.models import UserRoles


# Create your views here.


class CourseViewSet(viewsets.ModelViewSet):
    """ Для вывода информации (ViewSet-класс д)"""
    serializer_class = CourseSerializer
    #queryset = Course.objects.all()
    permission_classes = [IsAuthenticated, IsModeratorOrReadOnly | IsCourseOwner]
    pagination_class = LessonPaginator

    def perform_create(self, serializer):       # Модераторы не могут создавать обьект
        if self.request.user.role == UserRoles.MODERATOR:
            raise PermissionDenied("Вы не можете создавать новые курсы!")
        else:                                   # Функция привязывает автора к его курсу
            serializer.save()
            self.request.user.course_set.add(serializer.instance)

    def perform_destroy(self, instance):        # Модераторы не могут удалять обьект
        if self.request.user.role == UserRoles.MODERATOR:
            raise PermissionDenied("Вы не можете удалять курсы!")
        instance.delete()

    # Если user - не модератор, то функция показывает только его курсы
    def get_queryset(self):
        if self.request.user.role == UserRoles.MODERATOR:
            return Course.objects.all()
        else:
            return Course.objects.filter(author=self.request.user)


class LessonListAPIView(ListAPIView):
    """ Отображение списка сущностей (Generic-класс)"""
    serializer_class = LessonSerializer
    #queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModeratorOrReadOnly | IsCourseOrLessonOwner]
    pagination_class = LessonPaginator

    def get_queryset(self):       # Доступ к обьекту имеют только его владельцы и модератор
        if self.request.user.role == UserRoles.MODERATOR:
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(author=self.request.user)


class LessonRetrieveAPIView(RetrieveAPIView):
    """ Отображение одной сущности (Generic-класс)"""
    serializer_class = LessonSerializer
    #queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModeratorOrReadOnly | IsCourseOrLessonOwner]

    def get_queryset(self):
        if self.request.user.role == UserRoles.MODERATOR:
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(author=self.request.user)


class LessonCreateAPIView(CreateAPIView):
    """ Создание сущности (Generic-класс)"""
    serializer_class = LessonSerializer
    #queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModeratorOrReadOnly | IsCourseOrLessonOwner]

    def perform_create(self, serializer):      # Модераторы не могут создавать обьект
        if self.request.user.role == UserRoles.MODERATOR:
            raise PermissionDenied("Вы не можете создать новый урок!")
        new_lesson = serializer.save()         # Функция привязывает автора к его уроку
        new_lesson.author = self.request.user
        new_lesson.save()


class LessonUpdateAPIView(UpdateAPIView):
    """ Редактирование сущности (Generic-класс)"""
    serializer_class = LessonSerializer
    #queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == UserRoles.MODERATOR:
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(author=self.request.user)


class LessonDestroyAPIView(DestroyAPIView):
    """ Удаление сущности (Generic-класс)"""
    serializer_class = LessonSerializer
    #queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Доступ к обьекту имеют только его владельцы и модератор """
        if self.request.user.role == UserRoles.MODERATOR:
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(author=self.request.user)

    def perform_destroy(self, instance):
        """ Модераторы не могут удалять обьект """
        if self.request.user.role == UserRoles.MODERATOR:
            raise PermissionDenied("Вы не можете удалять уроки!")
        instance.delete()


class SubscriptionCreateAPIView(CreateAPIView):
    """ Создание сущности (Generic-класс_Подписка) """
    serializer_class = SubscriptionSerializer
    #queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated, IsModeratorOrReadOnly | IsCourseOrLessonOwner]

    def perform_create(self, serializer):
        serializer.save()
        self.request.user.subscription_set.add(serializer.instance)


class SubscriptionDestroyAPIView(DestroyAPIView):
    """ Удаление сущности (Generic-класс_Подписка) """
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]
