from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from study.models import Lesson, Course, Subscription
from users.models import User


class LessonApiTestCase(APITestCase):
    """ Тесты на CRUD урока"""
    def setUp(self) -> None:
        user = User.objects.create(email='test@test.test', is_active=True)
        user.set_password('test_password')
        user.save()
        response = self.client.post('/users/api/token/', data={"email": "test@test.test", "password": "test_password"})
        self.token = response.json()["access"]
        self.user = user

    def test_create_lesson(self):
        """ Тестирование создания урока """
        heard = {
            "Authorization": f"Bearer {self.token}"
        }
        course = Course.objects.create(
                                       title_course='Тестовый курс',
                                       description_course='Тест'
                                      )
        data = {
                "title_lesson": "Test",
                "description_lesson": "Test",
                "course": course.id
        }
        response = self.client.post('/study/lesson_create/create/', data=data, headers=heard)

        self.assertEqual(
                         response.status_code,
                         status.HTTP_201_CREATED
                        )

        self.assertTrue(Course.objects.all().exists())

    def test_list_lesson(self):
        """ Тестирование вывода списка уроков """
        course = Course.objects.create(
                                        title_course='Тестовый курс',
                                        description_course='Тест',
                                      )

        lesson = Lesson.objects.create(
                                        title_lesson='Тестовый урок',
                                        description_lesson='Тест',
                                        url_course=course,
                                        author=self.user
                                      )

        heard = {
            "Authorization": f"Bearer {self.token}"
        }

        response = self.client.get('/study/lesson_list/', headers=heard)

        self.assertEqual(
                         response.status_code,
                         status.HTTP_200_OK
                        )

    def test_retrieve_lesson(self):
        """ Тестирование вывода одного урока """
        course = Course.objects.create(
                                        title_course='Тестовый курс',
                                        description_course='Тест',
                                      )
        lesson = Lesson.objects.create(
                                        title_lesson='Тестовый урок',
                                        description_lesson='Тест',
                                        url_course=course,
                                        author=self.user
                                      )
        heard = {
            "Authorization": f"Bearer {self.token}"
        }

        response = self.client.get(f'/study/lesson_retrieve/{lesson.id}/', headers=heard)

        self.assertEqual(
                         response.status_code,
                         status.HTTP_200_OK
                        )

    def test_update_lesson(self):
        """ Тестирование редактирования урока """
        course = Course.objects.create(
                                        title_course='Тестовый курс',
                                        description_course='Тест',
                                      )
        lesson = Lesson.objects.create(
                                        title_lesson='Тестовый урок',
                                        description_lesson='Тест',
                                        url_course=course,
                                        author=self.user
                                      )

        heard = {
            "Authorization": f"Bearer {self.token}"
        }
        data = {
            'title_lesson': 'Test lesson update'
        }

        response = self.client.patch(f'/study/lesson_update/{lesson.id}/', data=data, headers=heard)

        self.assertEqual(
                         response.status_code,
                         status.HTTP_200_OK
                        )

        self.assertEqual(
                         response.json()['title_lesson'],
                         'Test lesson update'
                        )

    def test_delete_lesson(self):
        """ Тестирование удаления урока """
        course = Course.objects.create(
                                        title_course='Тестовый курс',
                                        description_course='Тест',
                                      )
        lesson = Lesson.objects.create(
                                        title_lesson='Тестовый урок',
                                        description_lesson='Тест',
                                        url_course=course,
                                        author=self.user
                                      )
        heard = {
            "Authorization": f"Bearer {self.token}"
        }

        response = self.client.delete(f'/study/lesson_destroy/{lesson.id}/', headers=heard)

        self.assertEqual(
                         response.status_code,
                         status.HTTP_204_NO_CONTENT
                        )


class SubscriptionTestCase(APITestCase):
    """ Тесты на создание и удаление подписки """
    def setUp(self) -> None:
        user = User.objects.create(email='test@test.test', is_active=True)
        user.set_password('test_password')
        user.save()
        response = self.client.post('/users/api/token/', data={"email": "test@test.test", "password": "test_password"})
        self.token = response.json()["access"]
        self.user = user

    def test_create_subscription(self):
        """ Тестирование создания подписки """
        heard = {
            "Authorization": f"Bearer {self.token}"
        }
        course = Course.objects.create(
                                        title_course='Тестовый курс',
                                        description_course='Тест',
                                      )
        data = {
            'course_subscription': course.id,
        }
        response = self.client.post('/study/subscription_create/', data=data, headers=heard)

        self.assertEqual(
                         response.status_code,
                         status.HTTP_201_CREATED
                        )

    def test_delete_subscription(self):
        """ Тестирование удаления подписки """
        heard = {
            "Authorization": f"Bearer {self.token}"
        }
        course = Course.objects.create(
                                        title_course='Тестовый курс',
                                        description_course='Тест',
                                      )
        subscription = Subscription.objects.create(
                                                    user=self.user,
                                                    course_subscription=course
                                                  )
        response = self.client.delete(f'/study/subscription_destroy/{subscription.id}/', headers=heard)

        self.assertEqual(
                         response.status_code,
                         status.HTTP_204_NO_CONTENT
                        )
