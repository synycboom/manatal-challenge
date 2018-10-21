from rest_framework import routers
from education.views import SchoolViewSet
from django.urls import path, include

router = routers.SimpleRouter()
router.register(r'schools', SchoolViewSet, basename='schools')

urlpatterns = [
    path('', include(router.urls))
]
