# from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from . import models


class UserSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'account_type')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        patient = models.Patient()
        patient.save()
        doctor = models.Doctor()
        doctor.save()
        inspector = models.Inspector()
        inspector.save()
        user = models.User.objects.create_user(**validated_data, patient=patient, doctor=doctor, inspector=inspector)
        return user


class PatientSerializer(ModelSerializer):
    class Meta:
        model = models.Patient
        fields = ('id', 'ecg', 'body_temp', 'spo2', 'heart_rate')


class DoctorSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = models.Doctor
        fields = ('id', 'user')


class InspectorSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = models.Inspector
        fields = ('id', 'user')


class RequestSerializer(ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = models.Request
        fields = ('id', 'sender', 'receiver', 'message', 'timestamp', 'status')
