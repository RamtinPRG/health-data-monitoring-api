from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate

from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import serializers


# Create your views here.

@api_view(['POST'])
def signup(request):
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
    if request.user.is_authenticated:
        return Response({'error': 'You are already logged in.'})
    else:
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'success': 'Logged in successfully.'})
        else:
            return Response({'error': 'Invalid username or password.'})


@api_view(['GET'])
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return Response({'success': 'Logged out successfully.'})
    else:
        return Response({'error': 'You are not logged in.'})


@api_view(['GET'])
def authentication_status(request):
    if request.user.is_authenticated:
        return Response({'authenticated': True})
    else:
        return Response({'authenticated': False})
