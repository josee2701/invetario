# accounts/urls.py

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import LoginAPIView, RegistrationAPIView, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('api/register/', RegistrationAPIView.as_view(), name='api-register'),
    path('api/login/',      LoginAPIView.as_view(),      name='api-login'),
    path('api/', include(router.urls)),
]
