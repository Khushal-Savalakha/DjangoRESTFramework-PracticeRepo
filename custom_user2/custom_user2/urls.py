
from django.contrib import admin
from django.urls import path
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/',views.signup),
    path('login/',views.login_user),
    path('csrf/',views.get_csrf_token),
    path('profile/',views.get_profile_data)
]
