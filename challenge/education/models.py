import os
import binascii
from django.db import models


class ConcurrentSavingError(ValueError):
    pass


class MaximumStudentsError(ValueError):
    pass


class School(models.Model):
    """
    NOTE: A try-except block for MaximumStudentsError is needed when saving
    """
    name = models.CharField(max_length=20)
    max_students = models.PositiveIntegerField()

    def __str__(self):
        return '{} {}'.format(self.name, self.max_students)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._max_students = self.max_students

    def is_full(self):
        return self.students.count() >= self.max_students

    def save(self, *args, **kwargs):
        if self.max_students < self.students.count():
            raise MaximumStudentsError()
        super().save(*args, **kwargs)


class Student(models.Model):
    """
    NOTE:
        1. A try-except block for IntegrityError is needed when creating a new student.
           There may be a collision occurs because the max length of the identification field
           is limited to 20 characters, we cannot use a UUID field which is 32 characters long.
        2. save() method also checks whether the number of students exceeds a max_students of a school.
        3. try-except blocks for MaximumStudentsError and ConcurrentSavingError are needed when saving
           because we have to check whether or not a school is full,
           and a bug can occur if there are concurrent requests
        4. Student.objects.filter(...).update(...) shouldn't be called because it will ignore the logic in save()
    """

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    identification = models.CharField(max_length=20, editable=False, unique=True)
    school = models.ForeignKey(School, related_name='students', on_delete=models.CASCADE)

    def __str__(self):
        return '{} {} {}'.format(
            self.identification,
            self.first_name,
            self.last_name,
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._initial_school = self.school if self.pk else None

    @staticmethod
    def generate_identification():
        """
        suggested by: https://stackoverflow.com/a/2782293
        :return: A 20-character string
        """
        maximum_retry = 10
        for _ in range(0, maximum_retry):
            identification = binascii.b2a_hex(os.urandom(10)).decode()

            if not Student.objects.filter(identification=identification).exists():
                break

        return identification

    def save(self, *args, **kwargs):
        # try to generate identification when creating a new student object
        if not self.pk:
            self.identification = self.generate_identification()

        # check maximum students and concurrent create/update when creating a new student object
        # or updating an existing student object of which the school is changed
        if not self.pk or self._initial_school != self.school:
            if self.school.is_full():
                raise MaximumStudentsError()

            prev_students_number = self.school.students.count()
            super().save(*args, **kwargs)
            curr_student_number = self.school.students.count()

            if curr_student_number != prev_students_number + 1:
                raise ConcurrentSavingError()
        else:
            super().save(*args, **kwargs)
