from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from education.factories import SchoolFactory
from education.models import School


class SchoolTests(APITestCase):
    def test_create_school(self):
        url = reverse('education:schools-list')
        data = {
            'name': 'school1',
            'max_students': 10,
        }
        response = self.client.post(url, data)
        school = School.objects.first()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertIsNotNone(school)
        self.assertEqual(school.name, data['name'])
        self.assertEqual(school.max_students, data['max_students'])

    def test_update_school(self):
        school = SchoolFactory(name='school1', max_students=5)
        url = reverse('education:schools-detail', args=[school.pk])
        data = {
            'name': 'school2',
            'max_students': 20,
        }
        response = self.client.put(url, data)
        school.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(school.name, data['name'])
        self.assertEqual(school.max_students, data['max_students'])

    def test_partial_update_school(self):
        school = SchoolFactory(max_students=5)
        name = school.name
        url = reverse('education:schools-detail', args=[school.pk])
        data = {
            'max_students': 20,
        }
        response = self.client.patch(url, data)
        school.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(school.name, name)
        self.assertEqual(school.max_students, data['max_students'])

    def test_delete_school(self):
        school = SchoolFactory()
        url = reverse('education:schools-detail', args=[school.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.data)
        self.assertEqual(School.objects.count(), 0)
