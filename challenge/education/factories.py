import factory
from factory import fuzzy
from education.models import School, Student


class SchoolFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = School

    name = fuzzy.FuzzyText(length=20)
    max_students = fuzzy.FuzzyInteger(1, 30)


class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Student

    first_name = fuzzy.FuzzyText(length=20)
    last_name = fuzzy.FuzzyText(length=20)
    school = factory.SubFactory(SchoolFactory)
