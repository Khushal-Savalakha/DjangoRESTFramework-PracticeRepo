from .models import Student
from .serializers import StudentSerializer
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

class StudentModelViewSet(viewsets.ModelViewSet):
    """
    A ModelViewSet for performing CRUD operations on the Student model.
    
    By default, it uses global settings for authentication and permission classes.
    To override these global settings for specific use cases, you can uncomment 
    the `authentication_classes` and `permission_classes` attributes and set them 
    as per your requirements.
    """
    queryset = Student.objects.all()  # Queryset to fetch all Student records.
    serializer_class = StudentSerializer  # Serializer to handle data validation and serialization.

    # Uncomment the following lines to override global authentication and permissions
    # authentication_classes = [BasicAuthentication]  # Use Basic Authentication for this viewset.
    # permission_classes = [IsAuthenticated]  # Allow access only to authenticated users.


"""
Example: Allow all users access regardless of authentication.

If most classes share the same permission settings globally, but an exception
is required for one or a few classes, you can override the global permissions
by explicitly defining `permission_classes` for those specific classes.

class StudentModelViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    authentication_classes = [BasicAuthentication]  # Use Basic Authentication.
    permission_classes = [AllowAny]  # Allow access to all users, including unauthenticated ones.
"""
"""
Example: Restrict access to staff users only (is_staff=True).

This configuration ensures that only users with the `is_staff` attribute set to `True`
are allowed to perform CRUD operations on the Student model.

class StudentModelViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    authentication_classes = [BasicAuthentication]  # Use Basic Authentication.
    permission_classes = [IsAdminUser]  # Restrict access to admin (staff) users only.
    
    # Note: If `is_staff=False`, the user will not have access to this viewset.
"""
