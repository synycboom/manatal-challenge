from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from education.factories import SchoolFactory, StudentFactory
from education.models import Student


class StudentTestCase(APITestCase):
    def test_create_student(self):
        school = SchoolFactory()
        data = {
            'first_name': 'John',
            'last_name': 'Cena',
            'school': school.id,
        }
        url = reverse('education:students-list')
        response = self.client.post(url, data)
        student = Student.objects.first()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertIsNotNone(student)
        self.assertEqual(student.first_name, data['first_name'])
        self.assertEqual(student.last_name, data['last_name'])
        self.assertEqual(student.school, school)
        self.assertNotEqual(student.identification, '')

    def test_update_student(self):
        new_school = SchoolFactory()
        student = StudentFactory(first_name='John', last_name='Cena')
        identification = student.identification
        data = {
            'first_name': 'John',
            'last_name': 'Wick',
            'school': new_school.pk,
        }
        url = reverse('education:students-detail', args=[student.pk])
        response = self.client.put(url, data)
        student.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(student.first_name, data['first_name'])
        self.assertEqual(student.last_name, data['last_name'])
        self.assertEqual(student.school, new_school)
        self.assertEqual(student.identification, identification)

    def test_partial_update_student(self):
        student = StudentFactory(first_name='John', last_name='Cena')
        identification = student.identification
        first_name = student.first_name
        school = student.school

        data = {
            'last_name': 'Wick',
        }
        url = reverse('education:students-detail', args=[student.pk])
        response = self.client.patch(url, data)
        student.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(student.last_name, data['last_name'])
        self.assertEqual(student.first_name, first_name)
        self.assertEqual(student.school, school)
        self.assertEqual(student.identification, identification)

    def test_delete_student(self):
        student = StudentFactory()
        url = reverse('education:students-detail', args=[student.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.data)
        self.assertEqual(Student.objects.count(), 0)

    def test_create_fail_due_to_maximum_student(self):
        school = SchoolFactory(max_students=1)
        StudentFactory(school=school)

        data = {
            'first_name': 'John',
            'last_name': 'Wick',
            'school': school.id,
        }
        url = reverse('education:students-list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(response.data, {'school': ['The school is full']})

    def test_update_fail_due_to_maximum_student(self):
        school = SchoolFactory(max_students=1)
        StudentFactory(school=school)
        student = StudentFactory()
        data = {
            'school': school.id,
        }
        url = reverse('education:students-detail', args=[student.pk])
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(response.data, {'school': ['The school is full']})
