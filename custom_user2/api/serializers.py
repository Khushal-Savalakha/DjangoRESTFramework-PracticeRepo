from .models import CustomUser
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


class CustomUserSerializers(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields="__all__"
    
    def create(self,validated_data):
        validated_data['password']=make_password(validated_data['password'])
        return super().create(validated_data)