from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from materials.models import Course, Lesson
from users.models import User


class TestLesson(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="test@test.ru",
        )
        self.user.set_password("test")
        self.user.save()
        self.course = Course.objects.create(
            title="Test",
            description="Test",
            owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title='Test',
            description='Test',
            owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_list_lessons(self):
        """Тестирование вывода списка уроков"""

        response = self.client.get(
            reverse('materials:lessons_list')
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        print(response.json())
        self.assertEquals(
            response.json(),
            {
                'count': 1,
                'next': None,
                'previous': None,
                'results': [
                    {
                        'id': self.lesson.id,
                        'title': self.lesson.title,
                        'preview': self.lesson.preview,
                        'description': self.lesson.description,
                        'link': self.lesson.link,
                        'course': self.lesson.course,
                        'owner': self.user.id
                    }
                ]
            }
        )

    def test_create_lesson(self):
        """Тестирование создания урока"""

        data = {
            "link": "https://rutube.ru/21313",
            "title": "Высшая",
            "description": "Считать",
            "course": self.course.pk,
        }
        response = self.client.post(
            '/lesson/create/',
            data=data
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_update_lesson(self):
        """Тестирование изменения урока"""
        lesson = Lesson.objects.create(
            title='Test_lesson',
            description='Test_lesson',
            owner=self.user
        )
        response = self.client.patch(
            f'/lesson/update/{lesson.id}/',
            {'description': 'change'}
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_delete_lesson(self):
        """Тестирование удаления урока"""
        lesson = Lesson.objects.create(
            title='Test_lesson',
            description='Test_lesson',
            owner=self.user
        )
        response = self.client.delete(
            f'/lesson/delete/{lesson.id}/'
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class SubscribeTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="test@test.ru",
        )
        self.course = Course.objects.create(
            title="Test",
            description="Test",
            owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_subscribe_to_course(self):
        """Тест на создание подписки на курс"""

        data = {
            "user": self.user.id,
            "course": self.course.id,
        }
        response = self.client.post(
            reverse('materials:subscribe_post'),
            data=data
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEquals(
            response.json(),
            {'message': 'Вы подписались на обновления курса'}
        )
