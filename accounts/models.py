from django.contrib.auth.models import User as DjangoUser
from django.db import models

# Create your models here.

class User(DjangoUser):
    username = None
    class Meta:
        proxy = True    # importante: indica que NO hay nueva tabla

    def __str__(self):
        # cuando hagas str(user), mostrará el email
        return self.email