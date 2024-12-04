from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.serializers import CustomUserSerializers
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404
from .models import CustomUser
from django.contrib.auth.hashers import check_password

@api_view(['POST'])
def signup(request):
    """
    Handle user signup using the custom user model.
    """
    serializer = CustomUserSerializers(data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'msg': 'User created successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    print(request)
    """
    Handle user login using the default authentication system.
    """
    u_email = request.data.get('email')
    u_password = request.data.get('password')
    print(f"----------------->email:{u_email} ,password:{u_password}")

    if not u_email or not u_password:
        return Response({'msg': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Use email as the username for authentication
    user = authenticate(request, email=u_email, password=u_password)
    print(user)
    if user is not None:
        auth_login(request, user)
        return Response({'msg': 'User logged in successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'msg': 'Invalid email or password.'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def get_profile_data(request):
    """
    Retrieve user profile data for the logged-in user.
    """
    if not request.user.is_authenticated:
        return Response({'msg': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = CustomUserSerializers(request.user)
    return Response({'user': serializer.data}, status=status.HTTP_200_OK)

from django.http import JsonResponse

@api_view(['GET'])
def get_csrf_token(request):
    """
    Return CSRF token to the client.
    """
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})
