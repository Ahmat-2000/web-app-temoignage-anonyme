from django_use_email_as_username.models import BaseUser, BaseUserManager
from django.db import models

class User(BaseUser):
    objects = BaseUserManager()
    #username = models.CharField(max_length=40,default="Inconnito")
    class Meta:
        db_table = 'utilisateurs'
