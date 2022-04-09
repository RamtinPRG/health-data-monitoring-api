from django.db import models
from django.contrib.auth.models import AbstractUser


def default_ecg_dictionary():
    return {"data": []}

# Create your models here.


class User(AbstractUser):
    ACCOUNT_TYPES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('inspector', 'Inspector'),
    )
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES, default='patient')
    patient = models.OneToOneField('Patient', on_delete=models.CASCADE, null=True, blank=True)
    doctor = models.OneToOneField('Doctor', on_delete=models.CASCADE, null=True, blank=True)
    inspector = models.OneToOneField('Inspector', on_delete=models.CASCADE, null=True, blank=True)


class Patient(models.Model):
    ecg = models.JSONField(default=default_ecg_dictionary)
    body_temp = models.FloatField(default=0)
    spo2 = models.FloatField(default=0)
    heart_rate = models.IntegerField(default=0)


class Doctor(models.Model):
    patients = models.ManyToManyField(Patient)


class Inspector(models.Model):
    patients = models.ManyToManyField(Patient)


class Request(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    sender_visisbility = models.BooleanField(default=True)
    receiver_visibility = models.BooleanField(default=True)
