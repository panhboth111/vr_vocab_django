from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import CustomUserManager
import datetime

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    username = models.CharField('username', max_length=100)
    level = models.IntegerField(default=1)
    sub_plan = models.CharField(default="Bronze", max_length = 20)
    sub_date = models.DateTimeField(null=True)
    last_request = models.DateTimeField(null=True, default='2020-01-01 06:00:00.000000-08:00')
    score = models.IntegerField(default=0)
    coin = models.IntegerField(default=0)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    def __str__(self):
        return self.email
        
class ForgotPassword(models.Model):
    email = models.EmailField()
    code = models.IntegerField()
    confirmed = models.BooleanField(default=False)

class Card(models.Model):
  card_num = models.CharField(max_length=200)
  exp_month = models.CharField(max_length=5)
  exp_year = models.CharField(max_length=5)
  cvc = models.CharField(max_length=5)
  sub_plan = models.CharField(max_length=20)
  amount = models.CharField(default = "0", max_length=5)
  email = models.CharField("email ads", max_length=50)