
from django.contrib import admin
from django.urls import path
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('studentlc/',views.LCStudentAPI.as_view()),
    path('studentrud/<int:pk>/',views.RUDStudentAPI.as_view())
]
