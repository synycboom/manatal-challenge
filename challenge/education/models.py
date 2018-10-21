from django.db import models


class School(models.Model):
    name = models.CharField(max_length=20)
    max_students = models.PositiveIntegerField()

    def __str__(self):
        return '{} {}'.format(self.name, self.max_students)


class Student(models.Model):
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
