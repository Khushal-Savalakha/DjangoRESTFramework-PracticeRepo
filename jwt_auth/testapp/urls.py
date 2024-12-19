from django.urls import path
from .views import student_list,register,user_login,user_logout

# Below urls for custom management of JWT authentication management
urlpatterns = [
    path('students/', student_list, name='student_list'),
    path('signup/',register,name='signup'),
    path('login/',user_login,name='login'),
    path('logout/', user_logout, name='logout'),
]
