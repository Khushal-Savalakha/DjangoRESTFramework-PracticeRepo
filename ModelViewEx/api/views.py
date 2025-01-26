from rest_framework.decorators import api_view

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import login, authenticate, logout
from rest_framework import status
from .models import User, Company, Employee
from .serializers import UserSerializer, CompanySerializer, EmployeeSerializer
from django.middleware.csrf import get_token


class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'], url_path='login', url_name='login', permission_classes=[AllowAny])
    def user_login(self, request):
        print(request.data)
        try:
            print("hello")
            # quit()
            # print(request.data.POST['email'])
            email = request.data.get('email')
            password = request.data.get('password')
            print("--->email",email)
            print("--->password",password)
            if email and password:
                user = authenticate(email=email, password=password)
                if user:
                    login(request, user)
                    if user.is_superuser:
                        return Response({"message": "SuperAdmin Logged in Successfully!"}, status=status.HTTP_200_OK)
                    elif user.is_staff:
                        return Response({"message": "Admin Logged in Successfully!"}, status=status.HTTP_200_OK)
                    else:
                        return Response({"message": "Employee Logged in Successfully!"}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Invalid credentials!"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Please provide email and password!"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], url_path='logout', url_name='user-logout', permission_classes=[IsAuthenticated])
    def user_logout(self, request):
        try:
            if request.user.is_authenticated:
                logout(request)
                return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "You are not logged in"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], url_path='signup', url_name='user-signup', permission_classes=[AllowAny])
    def user_signup(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            username = request.data.get('username')
            company_name = request.data.get('company_name')
            country = request.data.get('country')

            if email and password and username and company_name and country:
                # Check if the user is an admin and create the company
                user = User.objects.create_user(email=email, password=password, username=username, is_staff=True)
                company = Company.objects.create(user=user, name=company_name, country=country, status='active')
                
                return Response({
                    "message": "Admin created successfully with company!",
                    "company_id": company.id
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Please provide all required fields!"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    # @action(detail=False, methods=['GET'], url_path='csrf', url_name='csrf-token', permission_classes=[AllowAny])
    # def get_csrf_token(request):
    #     csrf_token = get_token(self.request)
    #     return Response({'csrfToken': csrf_token},status=200)

    @action(detail=False, methods=['GET'], url_path='csrf', url_name='csrf-token', permission_classes=[AllowAny])
    def get_csrf_token(self, request):
        csrf_token = get_token(request)
        return Response({'csrfToken': csrf_token}, status=200)



from django.views.decorators.csrf import csrf_exempt

class CompanyView(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['POST'], url_path='create_emp', url_name='create_employee', permission_classes=[IsAuthenticated])
    def create_employee(self, request):
        print("---->Entered.")
        try:
            user = request.user
            if not user.is_staff:
                return Response({"message": "Only admins can create employees!"}, status=status.HTTP_403_FORBIDDEN)
            print("Authenticated user Create Employee")
            # Validate required fields
            email = request.data.get('email')
            password = request.data.get('password')
            company_id = request.data.get('company_id')
            print("--->email:",email)
            print("--->Password:",password)
            if not email or not password or not company_id:
                return Response(
                    {"message": "Email, password, and company ID are required!"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Fetch the company based on company_id
            try:
                company = Company.objects.get(id=company_id, user=user)
            except Company.DoesNotExist:
                return Response(
                    {"message": "Invalid company ID or you are not authorized!"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Include company details and other provided data
            employee_data = {
                "company": company.id,  # Ensure company_id is included in employee data
                "email": email,
                "password": password,
                **request.data  # Add other optional fields from the request
            }

            # Validate and save the employee data using the serializer with partial=True
            employee_serializer = EmployeeSerializer(data=employee_data, partial=True)

            if employee_serializer.is_valid():
                employee_serializer.save()
                return Response(
                    {"message": "Employee created successfully!", "employee": employee_serializer.data},
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(employee_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)





@api_view(['POST'])
@csrf_exempt
def test(request):
    print(request.POST)
    print("hello")
    return True


# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from django.contrib.auth import login, authenticate, logout
# from .models import User, Company, Employee
# from .serializers import UserSerializer, CompanySerializer, EmployeeSerializer
# from django.middleware.csrf import get_token
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def user_login(request):
#     try:
#         print(request)
#         email = request.data.get('email')
#         password = request.data.get('password')
#         if email and password:
#             user = authenticate(email=email, password=password)
#             if user:
#                 login(request, user)
#                 if user.is_superuser:
#                     return Response({"message": "SuperAdmin Logged in Successfully!"}, status=status.HTTP_200_OK)
#                 elif user.is_staff:
#                     return Response({"message": "Admin Logged in Successfully!"}, status=status.HTTP_200_OK)
#                 else:
#                     return Response({"message": "Employee Logged in Successfully!"}, status=status.HTTP_200_OK)
#             else:
#                 return Response({"message": "Invalid credentials!"}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({"message": "Please provide email and password!"}, status=status.HTTP_400_BAD_REQUEST)
#     except Exception as e:
#         return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def user_logout(request):
#     try:
#         if request.user.is_authenticated:
#             logout(request)
#             return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
#         else:
#             return Response({"message": "You are not logged in"}, status=status.HTTP_400_BAD_REQUEST)
#     except Exception as e:
#         return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def user_signup(request):
#     try:
#         email = request.data.get('email')
#         password = request.data.get('password')
#         username = request.data.get('username')
#         company_name = request.data.get('company_name')
#         country = request.data.get('country')

#         if email and password and username and company_name and country:
#             user = User.objects.create_user(email=email, password=password, username=username, is_staff=True)
#             company = Company.objects.create(user=user, name=company_name, country=country, status='active')
#             return Response({"message": "Admin created successfully with company!"}, status=status.HTTP_201_CREATED)
#         else:
#             return Response({"message": "Please provide all required fields!"}, status=status.HTTP_400_BAD_REQUEST)
#     except Exception as e:
#         return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# @permission_classes([AllowAny])
# def get_csrf_token(request):
#     csrf_token = get_token(request)
#     return Response({'csrfToken': csrf_token}, status=200)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def create_employee(request):
#     try:
#         user = request.user
#         if not user.is_staff:
#             return Response({"message": "Only admins can create employees!"}, status=status.HTTP_403_FORBIDDEN)
        
#         company = Company.objects.get(user=user)
#         first_name = request.data.get('first_name')
#         last_name = request.data.get('last_name')
#         country = request.data.get('country')
#         engagement_type = request.data.get('engagement_type')
#         employment_type = request.data.get('employment_type')
#         nationality = request.data.get('nationality')
#         start_date = request.data.get('start_date')
#         monthly_rate = request.data.get('monthly_rate')
#         work_location = request.data.get('work_location')
#         billing_cycle = request.data.get('billing_cycle')
#         status = request.data.get('status')

#         employee = Employee.objects.create(
#             company=company,
#             first_name=first_name,
#             last_name=last_name,
#             country=country,
#             engagement_type=engagement_type,
#             employment_type=employment_type,
#             nationality=nationality,
#             start_date=start_date,
#             monthly_rate=monthly_rate,
#             work_location=work_location,
#             billing_cycle=billing_cycle,
#             status=status
#         )
#         return Response({"message": "Employee created successfully!"}, status=status.HTTP_201_CREATED)
#     except Exception as e:
#         return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def test(request):
#     print(request.POST)
#     print("hello")
#     return Response({"message": "Test successful!"}, status=200)