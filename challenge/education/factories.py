import factory
from factory import fuzzy
from education.models import School


class SchoolFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = School

    name = fuzzy.FuzzyText(length=20)
    max_students = fuzzy.FuzzyInteger(1, 30)
