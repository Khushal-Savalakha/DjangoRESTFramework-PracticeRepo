from django.contrib import admin
from .models import User,Company,Employee

# Register your models here.
admin.site.register(User)
admin.site.register(Company)
admin.site.register(Employee)