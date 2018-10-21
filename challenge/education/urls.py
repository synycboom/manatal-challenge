from rest_framework_nested import routers
from education.views import SchoolViewSet, StudentViewSet
from django.urls import path, include

router = routers.SimpleRouter()
router.register(r'schools', SchoolViewSet, basename='schools')
router.register(r'students', StudentViewSet, basename='students')

nested_router = routers.NestedSimpleRouter(router, r'schools', lookup='school')
nested_router.register(r'students', StudentViewSet, basename='school-students')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(nested_router.urls))
]
