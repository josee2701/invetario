# accounts/urls.py
from django.urls import include, path
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.routers import DefaultRouter

from .views import LoginAPIView, UserViewSet


class CustomRouter(DefaultRouter):
    def get_api_root_view(self, api_urls=None):
        # obtenemos la vista original de DefaultRouter
        api_root = super().get_api_root_view(api_urls)
        def custom_api_root(request, *args, **kwargs):
            # llamamos a la vista original y capturamos la data
            response = api_root(request, *args, **kwargs)
            # agregamos nuestros endpoints custom
            response.data['login']    = reverse('api-login',    request=request, format=kwargs.get('format'))
            return response
        return custom_api_root

router = CustomRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('api/login/',      LoginAPIView.as_view(),      name='api-login'),
    path('api/', include(router.urls)),
]
