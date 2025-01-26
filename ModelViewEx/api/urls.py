from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import UserView,CompanyView,test
router=DefaultRouter()

router.register(r'',UserView,basename='user-auth')
router.register(r'employee',CompanyView,basename="create-emp")

urlpatterns = [
    path('test/', test, name='test'),
]
urlpatterns+=router.urls


# from django.urls import path
# from . import views

# urlpatterns = [
#     path('login/', views.user_login, name='user-login'),
#     path('logout/', views.user_logout, name='user-logout'),
#     path('signup/', views.user_signup, name='user-signup'),
#     path('csrf/', views.get_csrf_token, name='csrf-token'),
#     path('create-employee/', views.create_employee, name='create-employee'),
#     path('test/', views.test, name='test'),
# ]