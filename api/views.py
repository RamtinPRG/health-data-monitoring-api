from urllib import response
from django.dispatch import receiver
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from . import serializers, models


# Create your views here.

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['id'] = user.id
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['email'] = user.email
        token['account_type'] = user.account_type

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def signup(request):
    """
    Creates an account based on the payload of request and
    checks the availability of username and validates the data.
    """
    if request.user.is_authenticated:
        return Response({'error': 'You are already logged in.'})
    else:
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()
            return Response(serializer.data)
        else:
            errors = serializer.errors
            errors['error'] = 'Invalid data'
            return Response(errors)


@api_view(['POST'])
def login_view(request):
    """
    Logs in an account based on the payload of request and
    the ability of login.
    This function (view) doesn't work since the authentication method
    is Json Web Token (JWT) and needs the access token.
    """
    if request.user.is_authenticated:
        return Response({'error': 'You are already logged in.'})
    else:
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            serializer = serializers.UserSerializer(user, request.data)
            if serializer.is_valid():
                login(request, user)
                data = serializer.data
                data['success'] = 'Logged in successfully.'
                return Response(data)
            else:
                errors = serializer.errors
                errors['error'] = 'Invalid data'
                return Response(errors)
        else:
            return Response({'error': 'Invalid username or password.'})


@api_view(['GET'])
def logout_view(request):
    """
    Logs out the authorized user.
    This function (view) doesn't work since the authentication method
    is Json Web Token (JWT) and needs the access token.
    """
    if request.user.is_authenticated:
        logout(request)
        return Response({'success': 'Logged out successfully.'})
    else:
        return Response({'error': 'You are not logged in.'})


@api_view(['GET'])
def authentication_status(request):
    """
    Checks if the user is authenticated.
    """
    if request.user.is_authenticated:
        return Response({'authenticated': True})
    else:
        return Response({'authenticated': False})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def doctors_view(request):
    """
    Returns a list of all doctors that has access to
    the authorized patient.
    It means it doesn't return the doctors for an unknown account.
    """
    if request.user.account_type == 'patient':
        doctors = request.user.patient.doctor_set.all()
        serializer = serializers.DoctorSerializer(doctors, many=True)
        return Response(serializer.data)
    else:
        return Response({'error': 'access denied'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def inspectors_view(request):
    """
    Returns a list of all inspectors that has access to
    the authorized patient.
    """
    if request.user.account_type == 'inspector':
        inspectors = request.user.inspector.patient_set.all()
        serializer = serializers.InspectorSerializer(inspectors, many=True)
        return Response(serializer.data)
    else:
        return Response({'error': 'access denied'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def patients_view(request):
    """
    Returns a list of all patients that the authorized
    account (inspector or doctor) has access to.
    """
    if request.user.account_type == 'doctor':
        patients = request.user.doctor.patients.all()
    elif request.user.account_type == 'inspector':
        patients = request.user.inspector.patients.all()
    else:
        return Response({'error': 'access denied'})
    serializer = serializers.PatientSerializer(patients, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def doctor_view(request, pk):
    """
    Returns a doctor based on the id of the doctor.
    """
    if request.user.account_type == 'patient':
        doctor = request.user.patient.doctor_set.filter(pk=pk)
        if len(doctor) != 0:
            serializer = serializers.DoctorSerializer(doctor)
            return Response(serializer.data)
    return Response({'error': 'access denied'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def patient_view(request, pk):
    """
    Returns a patient based on the id of the patient.
    """
    if models.User.objects.filter(pk=pk, account_type='patient').exists():
        patient = models.User.objects.get(pk=pk).patient
        serializer = serializers.PatientSerializer(patient)
        return Response(serializer.data)
    else:
        return Response({'error': 'patient not found'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def inspector_view(request, pk):
    """
    Returns an inspector based on the id of the inspector.
    """
    if request.user.account_type == 'patient':
        inspector = request.user.patient.inspector_set.filter(pk=pk)
        if inspector.exists():
            serializer = serializers.InspectorSerializer(inspector)
            return Response(serializer.data)
    return Response({'error': 'access denied'})


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def request_by_id_view(request, pk):
    """
    Returns or deletes a request based on the id of the request.
    """
    request_object = models.Request.objects.filter(pk=pk)
    if request_object.exists():
        request_object = request_object.first()
        if request.user.account_type == 'patient':
            if request_object.reciever == request.user:
                if request.method == 'GET':
                    serializer = serializers.RequestSerializer(request_object)
                    return Response(serializer.data)
                elif request.method == 'DELETE':
                    request_object.delete()
                    return Response({'success': 'request deleted successfully'})
            else:
                return Response({'error': 'access denied'})
        else:
            if request_object.sender == request.user:
                if request.method == 'GET':
                    serializer = serializers.RequestSerializer(request_object)
                    return Response(serializer.data)
                elif request.method == 'DELETE':
                    request_object.delete()
                    return Response({'success': 'request deleted successfully'})
            else:
                return Response({'error': 'access denied'})
    else:
        return Response({'error': 'request not found'})
    return Response({'error': 'access denied'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_view(request):
    """
    Creates a new request in the database with
    a specific sender, reciever and message.
    """
    receiver = models.User.objects.filter(username=request.data.get('username'))
    if not receiver.exists():
        return Response({'error': 'receiver not found'})
    receiver = receiver.first()
    if request.user.account_type != 'patient' and receiver.account_type == 'patient':
        if models.Request.objects.filter(sender=request.user, receiver=receiver, status='pending').exists():
            return Response({'error': 'request has already been sent'})
        else:
            request_object = models.Request(sender=request.user, receiver=receiver, status='pending')
            request_object.save()
            serializer = serializers.RequestSerializer(request_object)
            data = serializer.data
            data['success'] = 'request sent'
            return Response(data)
    else:
        return Response({'error': 'access denied'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def requests_view(request):
    """
    Returns a list of all requests that the authorized
    account has sent or received.
    """
    if request.user.account_type == 'patient':
        requests = models.Request.objects.filter(receiver=request.user)
    else:
        requests = models.Request.objects.filter(sender=request.user)
    serializer = serializers.RequestSerializer(requests, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_request_view(request):
    if request.user.account_type == 'patient':
        request_object = models.Request.objects.filter(pk=request.data.get('id'))
        if request_object.exists():
            request_object = request_object.first()
            if request_object.status == 'pending':
                request_object.status = 'accepted'
                request_object.save()
                sender = request_object.sender
                if sender.account_type == 'doctor':
                    sender.doctor.patients.add(request_object.receiver.patient)
                elif sender.account_type == 'inspector':
                    sender.inspector.patients.add(request_object.receiver.patient)
                serializer = serializers.RequestSerializer(request_object)
                data = serializer.data
                data['success'] = 'request accepted'
                return Response(data)
            else:
                return Response({'error': 'request has already been accepted or rejected'})
        else:
            return Response({'error': 'request not found'})
    else:
        return Response({'error': 'access denied'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_request_view(request):
    """
    Rejects a request based on the id of the request.
    """
    if request.user.account_type == 'patient':
        request_object = models.Request.objects.filter(pk=request.data.get('id'))
        if request_object.exists():
            request_object = request_object.first()
            if request_object.status == 'pending':
                request_object.status = 'rejected'
                request_object.save()
                serializer = serializers.RequestSerializer(request_object)
                data = serializer.data
                data['success'] = 'request rejected'
                return Response(data)
            else:
                return Response({'error': 'request has already been accepted or rejected'})
        else:
            return Response({'error': 'request not found'})
    else:
        return Response({'error': 'access denied'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_visibility_view(request, pk):
    """
    Changes the visibility of a request based on the id of the request.
    """
    request_object = models.Request.objects.filter(pk=pk)
    if request_object.exists():
        request_object = request_object.first()
        if request.user.account_type == 'patient':
            if request_object.reciever == request.user:
                request_object.reciever_visibility = request.data.get('visibility')
                request_object.save()
                serializer = serializers.RequestSerializer(request_object)
                return Response(serializer.data)
            else:
                return Response({'error': 'access denied'})
        else:
            if request_object.sender == request.user:
                request_object.sender_visibility = request.data.get('visibility')
                request_object.save()
                serializer = serializers.RequestSerializer(request_object)
                return Response(serializer.data)
            else:
                return Response({'error': 'access denied'})
    else:
        return Response({'error': 'request not found'})
