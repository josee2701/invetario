from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

# Create your models here.

class User(AbstractUser):
    username = None
    
    email = models.EmailField('Correo electrónico', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    
    def __str__(self):
        return self.email