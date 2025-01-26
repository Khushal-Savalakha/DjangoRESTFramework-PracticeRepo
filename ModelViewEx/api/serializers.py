from rest_framework import serializers
from .models import User, Company, Employee

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


# Company Serializer
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'user', 'name', 'status', 'country']
        read_only_fields = ['user']  # user is set automatically



from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            'id', 'company', 'first_name', 'last_name', 'email', 'country', 
            'engagement_type', 'employment_type', 'nationality', 'start_date', 
            'end_date', 'monthly_rate', 'work_location', 'billing_cycle', 
            'documents', 'status', 'password'
        ]

    def create(self, validated_data):
        # Manually hash the password before saving
        password = validated_data.get('password')
        if password:
            validated_data['password'] = make_password(password)  # Hash the password

        # Create the employee instance with the hashed password
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Hash the password if it's being updated
        password = validated_data.get('password')
        if password:
            validated_data['password'] = make_password(password)

        # Proceed with updating the instance
        return super().update(instance, validated_data)
