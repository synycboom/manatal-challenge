from rest_framework_nested import routers
from education import views
from django.urls import path, include

router = routers.SimpleRouter()
router.register(r'schools', views.SchoolViewSet, basename='schools')
router.register(r'students', views.StudentViewSet, basename='students')
router.register(r'nationalities', views.NationalityViewSet, basename='nationalities')

nested_router = routers.NestedSimpleRouter(router, r'schools', lookup='school')
nested_router.register(r'students', views.StudentViewSet, basename='school-students')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(nested_router.urls))
]
