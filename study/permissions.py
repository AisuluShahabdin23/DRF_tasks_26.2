from rest_framework import permissions
from users.models import UserRoles
#from rest_framework.permissions import BasePermission


class IsModeratorOrReadOnly(permissions.BasePermission):
    """ Модератор или только чтение """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == UserRoles.MODERATOR


class IsCourseOwner(permissions.BasePermission):
    """ Владелец курса """
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsCourseOrLessonOwner(permissions.BasePermission):
    """ Владелец курса или урока """
    def has_object_permission(self, request, view, obj):
        return obj.course.author == request.user or obj.course.lesson_set.filter(author=request.user).exists()


class IsPaymentOwner(permissions.BasePermission):
    """ Владелец платежа """
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
