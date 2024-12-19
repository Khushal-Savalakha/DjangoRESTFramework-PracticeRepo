from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Student
from testapp.serializers import StudentSerializer,UserSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate,login as auth_login

@api_view(['POST'])
def register(request):
    try:
        serializer=UserSerializer(data=request.data,partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response()
    except BaseException as error:
        return Response({error},status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_login(request):
    try:
        user=authenticate(request,username=request.data.get('username'),password=request.data.get('password'))
        if user is not None:
            auth_login(request,user)
            refresh = RefreshToken.for_user(user)
            return Response(
                {'refresh':str(refresh),
                 'access':str(refresh.access_token)},status=status.HTTP_200_OK)
        else:
            return Response({'msg':'user is not created.'},status=status.HTTP_404_NOT_FOUND)
    except BaseException as error:
        return Response({error},status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    try:
        # Extract refresh token from the request
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"error": "Refresh token is required for logout."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Blacklist the refresh token
        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response({"msg": "Successfully logged out."}, status=status.HTTP_200_OK)
    except Exception as error:
        return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# View to GET all student data or POST new student data
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def student_list(request):
    if request.method == 'GET':
        # Retrieve all student records
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        # Add a new student record
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
