from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, LocationViewSet, SkillViewSet

router = DefaultRouter()

router.register(r'location', LocationViewSet)
router.register(r'skill', SkillViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('profile', UserProfileViewSet.as_view({
        'get': 'list',
        'put': 'update',
    })),
]
