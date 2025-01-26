from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'  # Set email as the unique identifier
    REQUIRED_FIELDS = ['username']  # Ensure email is not in REQUIRED_FIELDS

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'auth_user'


class Company(models.Model):
    class StatusEnum(models.TextChoices):
        ACTIVE = 'active', _('Active')
        INACTIVE = 'inactive', _('Inactive')
        PENDING = 'pending', _('Pending')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='companies')  # One Admin can create multiple companies
    name = models.CharField(max_length=30)
    status = models.CharField(choices=StatusEnum.choices, max_length=10)
    country = models.CharField(max_length=80)

    def __str__(self):
        return self.name


# class Employee(models.Model):
#     class EmploymentTypeEnum(models.TextChoices):
#         EOR_EMPLOYEE = 'EOR employee', _('EOR Employee')
#         EOR_CONTRACTOR = 'EOR contractor', _('EOR Contractor')

#     class WorkStatusEnum(models.TextChoices):
#         ACTIVE = 'active', _('Active')
#         INACTIVE = 'inactive', _('Inactive')

#     company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employees')  # A company can have multiple employees
#     first_name = models.CharField(max_length=90)
#     last_name = models.CharField(max_length=90)
#     country = models.CharField(max_length=80)
#     engagement_type = models.CharField(max_length=100, default=None)
#     employment_type = models.CharField(choices=EmploymentTypeEnum.choices,default=None, max_length=20)
#     nationality = models.CharField(max_length=20, default=None)
#     start_date = models.DateField()
#     end_date = models.DateField(null=True, blank=True)
#     monthly_rate = models.FloatField()
#     work_location = models.CharField(max_length=20)
#     billing_cycle = models.CharField(max_length=20)
#     documents = models.FileField(upload_to='employee_documents/', blank=True, null=True)  # Optional file uploads
#     status = models.CharField(choices=WorkStatusEnum.choices,default=None, max_length=10)
#     password = models.CharField(max_length=255)  # Could be hashed password or token

#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"


class Employee(models.Model):
    class EmploymentTypeEnum(models.TextChoices):
        EOR_EMPLOYEE = 'EOR employee', _('EOR Employee')
        EOR_CONTRACTOR = 'EOR contractor', _('EOR Contractor')

    class WorkStatusEnum(models.TextChoices):
        ACTIVE = 'active', _('Active')
        INACTIVE = 'inactive', _('Inactive')

    company = models.ForeignKey(
        'Company',
        on_delete=models.CASCADE,
        related_name='employees'
    )  # A company can have multiple employees
    first_name = models.CharField(max_length=90, null=True, blank=True)
    last_name = models.CharField(max_length=90, null=True, blank=True)
    email = models.EmailField(unique=True)  # Added email field
    country = models.CharField(max_length=80, null=True, blank=True)
    engagement_type = models.CharField(max_length=100, default=None, null=True, blank=True)
    employment_type = models.CharField(
        choices=EmploymentTypeEnum.choices, max_length=20, null=True, blank=True
    )
    nationality = models.CharField(max_length=20, default=None, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    monthly_rate = models.FloatField(null=True, blank=True)
    work_location = models.CharField(max_length=20, null=True, blank=True)
    billing_cycle = models.CharField(max_length=20, null=True, blank=True)
    documents = models.FileField(
        upload_to='employee_documents/', blank=True, null=True
    )  # Optional file uploads
    status = models.CharField(
        choices=WorkStatusEnum.choices, max_length=10, null=True, blank=True
    )
    password = models.CharField(max_length=255)

    def _str_(self):
        return f"{self.first_name or ''} {self.last_name or ''}".strip()

