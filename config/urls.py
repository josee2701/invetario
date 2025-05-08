from django.contrib import admin
from django.urls import include, path
from rest_framework.reverse import reverse
from rest_framework.routers import DefaultRouter

from accounts.views import LoginAPIView, UserViewSet
from company.views import CompanyViewSet


class CustomRouter(DefaultRouter):
    def get_api_root_view(self, api_urls=None):
        api_root = super().get_api_root_view(api_urls)
        def custom_api_root(request, *args, **kwargs):
            response = api_root(request, *args, **kwargs)
            # agregamos nuestro endpoint de login
            response.data['login'] = reverse('api-login', request=request, format=kwargs.get('format'))
            return response
        return custom_api_root

# Usamos sólo el CustomRouter
router = CustomRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'companies', CompanyViewSet, basename='company')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('api/login/', LoginAPIView.as_view(), name='api-login'),
]
