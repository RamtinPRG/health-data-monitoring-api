from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Nurse(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
