from django.db import models

# Create your models here.

class Company(models.Model):
    nit = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    