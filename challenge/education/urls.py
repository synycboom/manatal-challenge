from rest_framework import routers
from education.views import SchoolViewSet, StudentViewSet
from django.urls import path, include

router = routers.SimpleRouter()
router.register(r'schools', SchoolViewSet, basename='schools')
router.register(r'students', StudentViewSet, basename='students')

urlpatterns = [
    path('', include(router.urls))
]
