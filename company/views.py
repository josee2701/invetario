# companies/views.py

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated  # o la que quieras
from rest_framework.response import Response

from products.models import Product
from products.serializers import ProductSerializer

from .models import Company
from .serializers import CompanySerializer


class CompanyViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para Company.
    Sólo usuarios autenticados pueden acceder.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    @action(detail=True, methods=['get'], url_path='products')
    def products(self, request, pk=None):
        # aquí devolvemos los productos de la compañía `pk`
        qs = Product.objects.filter(company_id=pk)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = ProductSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = ProductSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)
