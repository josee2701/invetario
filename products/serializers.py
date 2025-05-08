# products/serializers.py

from rest_framework import serializers

from company.models import Company
from company.serializers import CompanySerializer

from .models import Product, Stock


class ProductNestedSerializer(serializers.ModelSerializer):
    """
    Serializer ligero para evitar recursión al anidar dentro de StockSerializer
    """
    class Meta:
        model = Product
        fields = ('cod', 'name', 'price_cop', 'price_usd')

class StockSerializer(serializers.ModelSerializer):
    # Campo writable: recibe el PK del producto
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )
    # Campo read-only nested: usa ProductNestedSerializer para romper recursión
    product_detail = ProductNestedSerializer(source='product', read_only=True)

    class Meta:
        model = Stock
        fields = ('id', 'quantity', 'date', 'product', 'product_detail')

class ProductSerializer(serializers.ModelSerializer):
    # Para escritura: PK de Company
    company = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all()
    )
    # Para lectura: detalle completo de Company
    company_detail = CompanySerializer(source='company', read_only=True)
    # Listado de stocks asociados
    stock = StockSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            'cod',
            'name',
            'characteristics',
            'price_cop',
            'price_usd',
            'company',
            'company_detail',
            'stock',
        )
