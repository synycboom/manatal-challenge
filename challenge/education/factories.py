import factory
from factory import fuzzy
from education.models import School, Student, Nationality


class NationalityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Nationality

    name = fuzzy.FuzzyText(length=20)


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
    nationality = factory.SubFactory(NationalityFactory)
    school = factory.SubFactory(SchoolFactory)
