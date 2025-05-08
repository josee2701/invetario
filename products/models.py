from django.db import models

from company.models import Company

# Create your models here.

class Product(models.Model):
    cod = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    characteristics = models.TextField()
    price_cop = models.DecimalField(max_digits=10, decimal_places=2)
    price_usd = models.DecimalField(max_digits=10, decimal_places=2)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='product')

    def __str__(self):
        return f"{self.name} ({self.cod})"
    

class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE , related_name='stock')
    quantity = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.product} - {self.quantity} - {self.date}'
