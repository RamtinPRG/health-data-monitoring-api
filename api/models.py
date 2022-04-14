from django.db import models
from django.contrib.auth.models import AbstractUser


def default_ecg_dictionary():
    return {"data": []}

# Create your models here.


class User(AbstractUser):
    """
    User model inherited from AbstractUser model
    with other specific field.
    1- account type: saves the type of account (patient, inspector, doctor)
    2- Three one to one relationship with Patient, Doctor and Inspector models
    """
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
    """
    Saves the patient's health data.
    """
    ecg = models.JSONField(default=default_ecg_dictionary)
    body_temp = models.FloatField(default=0)
    spo2 = models.FloatField(default=0)
    heart_rate = models.IntegerField(default=0)


class Doctor(models.Model):
    """
    Saves all the patients that the doctor is handling (if the account type is doctor).
    """
    patients = models.ManyToManyField(Patient)


class Inspector(models.Model):
    """
    Saves all the patients that the account is inspecting (if the account type is inspector).
    """
    patients = models.ManyToManyField(Patient)


class Request(models.Model):
    """
    Requests that have been created by users.
    1- sender
    2- receiver
    3- message
    4- timestamp
    5- status
    """
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
