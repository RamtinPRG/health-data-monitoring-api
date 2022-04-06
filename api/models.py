from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    ACCOUNT_TYPES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('nurse', 'Nurse'),
    )
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES, default='patient')
    patient = models.OneToOneField('Patient', on_delete=models.CASCADE)
    doctor = models.OneToOneField('Doctor', on_delete=models.CASCADE)
    inspector = models.OneToOneField('Inspector', on_delete=models.CASCADE)


class Patient(models.Model):
    ecg = models.JSONField(default={'data': []})


class Doctor(models.Model):
    patients = models.ManyToManyField(Patient)


class Inspector(models.Model):
    patients = models.ManyToManyField(Patient)
