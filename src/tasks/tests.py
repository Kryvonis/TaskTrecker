from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth.models import User

from src.tasks.models import Task


class UsersTests(APITestCase):
    def setUp(self):
        user = User.objects.create(username='firstUser')
        user.set_password('12345')
        user.save()
        user = User.objects.create(username='secondUser')
        user.set_password('12345')
        user.save()

    def test_unauthorized_accounts(self):
        """
        Ensure we can't get objects without authorization.
        """
        url = '/api/v1/users/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorized_accounts(self):
        """
        Ensure we can't get objects without authorization.
        """

        url = '/api/v1/users/'

        self.client.login(username='firstUser', password='12345')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrive_unauthorize_tasks(self):
        """
        Ensure we can't get objects without authorization.
        """
        url = '/api/v1/tasks/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrive_authorize_tasks(self):
        """
        Ensure we can't get objects without authorization.
        """
        url = '/api/v1/tasks/'
        self.client.login(username='firstUser', password='12345')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_tasks(self):
        """
        Ensure we can create object.
        """
        url = '/api/v1/tasks/'
        self.client.login(username='firstUser', password='12345')

        task = {
            "name": "TestTask",
            "description": "",

        }

        response = self.client.post(url, task, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_tasks_with_user(self):
        """
        Ensure we can create object with user.
        """
        url = '/api/v1/tasks/'
        self.client.login(username='firstUser', password='12345')
        secondUser = User(username='secondUser')
        task = {
            "name": "TestTask",
            "description": "",
            "author": secondUser.id,
        }

        response = self.client.post(url, task, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cant_update_not_your_task(self):
        """
        Ensure we can't update object with another user.
        """
        url = '/api/v1/tasks/'
        self.client.login(username='firstUser', password='12345')
        secondUser = User.objects.get(username='secondUser')
        task = {
            "name": "TestTask",
            "description": "",
            "author": secondUser.id,
        }

        response = self.client.post(url, task, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = '/api/v1/tasks/1/'
        response = self.client.put(url, task, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cant_delete_not_your_task(self):
        """
        Ensure we can't update object with another user.
        """
        url = '/api/v1/tasks/'
        self.client.login(username='firstUser', password='12345')
        secondUser = User.objects.get(username='secondUser')
        task = {
            "name": "TestTask",
            "description": "",
            "author": secondUser.id,
        }

        response = self.client.post(url, task, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = '/api/v1/tasks/1/'
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)