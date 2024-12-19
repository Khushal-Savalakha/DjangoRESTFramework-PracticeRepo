from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Student(models.Model):
    name=models.CharField(max_length=250)
    roll_no=models.IntegerField()
    subject=models.CharField(max_length=250)


