from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import CustomUserManager
import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    username = models.CharField('username', max_length=100)
    level = models.IntegerField(default=0)
    sub_plan = models.CharField(default="Bronze", max_length = 20)
    sub_date = models.DateTimeField(default = timezone.now)
    last_request = models.DateTimeField(null=True, default=timezone.now().date()+relativedelta(days=-1))
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