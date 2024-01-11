from django.urls import path
from rest_framework.routers import DefaultRouter
from study.apps import StudyConfig
from study.views import CourseViewSet, LessonListAPIView, LessonRetrieveAPIView, LessonCreateAPIView, \
  LessonUpdateAPIView, LessonDestroyAPIView, SubscriptionCreateAPIView, SubscriptionDestroyAPIView

app_name = StudyConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
  path('lesson_list/', LessonListAPIView.as_view(), name='lesson_list'),
  path('lesson_retrieve/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_retrieve'),
  path('lesson_create/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
  path('lesson_update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
  path('lesson_destroy/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_destroy'),
  path('subscription_create/', SubscriptionCreateAPIView.as_view(), name='subscription_create'),
  path('subscription_destroy/<int:pk>/', SubscriptionDestroyAPIView.as_view(), name='subscription_destroy'),
] + router.urls
