from django.db import IntegrityError
from rest_framework import serializers
from education.models import School, Student, MaximumStudentsError, ConcurrentSavingError, Nationality


class NationalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Nationality
        fields = '__all__'


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'

    def update(self, instance, validated_data):
        try:
            instance = super().update(instance, validated_data)
        except MaximumStudentsError:
            raise serializers.ValidationError({
                'max_students': ['The number of students exceeds the maximum students']
            })
        return instance


class StudentSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(read_only=True)
    school_name = serializers.CharField(read_only=True, source='school.name')
    nationality_name = serializers.CharField(read_only=True, source='nationality.name')

    class Meta:
        model = Student
        fields = '__all__'

    def save(self, **kwargs):
        try:
            instance = super().save(**kwargs)
        except MaximumStudentsError:
            raise serializers.ValidationError({
                'school': ['The school is full']
            })
        except ConcurrentSavingError:
            raise serializers.ValidationError({
                'school': ['Unable to update the school due to concurrent requests, please try again']
            })
        except IntegrityError:
            raise serializers.ValidationError({
                'identification': ['Unable to generate identification, please try again']
            })
        return instance
