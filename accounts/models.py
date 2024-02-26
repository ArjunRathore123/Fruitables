from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import CustomManager
from django.utils import timezone
# Create your models here.

class CustomUser(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(unique=True)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    contact=models.CharField(max_length=10)
    choice=(('male','Male'),('female','Female'),('other','Other'))
    gender=models.CharField(max_length=6,choices=choice)
    address=models.TextField()
    created_at=models.DateTimeField(default=timezone.now)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)

    objects=CustomManager()

    USERNAME_FIELD= "email"
    REQUIRED_FIELDS=[]

    def __str__(self):
        return self.email