from rest_framework import viewsets
from education.models import School, Student, Nationality
from education.serializers import SchoolSerializer, StudentSerializer, NationalitySerializer


class NationalityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NationalitySerializer
    queryset = Nationality.objects.all()


class SchoolViewSet(viewsets.ModelViewSet):
    serializer_class = SchoolSerializer
    queryset = School.objects.all()
    filterset_fields = {
        'name': ('exact', 'icontains'),
        'max_students': ('exact', 'lt', 'lte', 'gt', 'gte'),
    }
    search_fields = ('name',)
    ordering_fields = ('name', 'max_students')


class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    filterset_fields = {
        'first_name': ('exact', 'icontains'),
        'last_name': ('exact', 'icontains'),
        'birth_date': ('exact',),
        'school__name': ('exact', 'icontains'),
        'school__max_students': ('exact', 'lt', 'lte', 'gt', 'gte'),
        'nationality__name': ('exact', 'icontains'),
    }
    search_fields = ('first_name', 'last_name')
    ordering_fields = (
        'first_name',
        'last_name',
        'birth_date',
        'school__name',
        'school__max_students',
        'nationality__name',
    )

    def get_queryset(self):
        queryset = self.queryset
        school_pk = self.kwargs.get('school_pk', None)

        if school_pk:
            queryset = queryset.filter(school=school_pk)

        return queryset

    def get_serializer(self, *args, **kwargs):
        school_pk = self.kwargs.get('school_pk', None)

        if school_pk and 'data' in kwargs:
            kwargs['data'] = {'school': school_pk, **kwargs['data'].dict()}

        return super().get_serializer(*args, **kwargs)
