# companies/views.py

from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Company
from .serializers import CompanySerializer


class CompanyViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para Company.
    Sólo usuarios autenticados pueden acceder.
    Si quieres restringir create/update/delete a Admin, puedes usar
    IsAdminUser o un permission custom.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
