from django.contrib import admin
from django.urls import path
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('studentlist/',views.StudentList.as_view()),
    path('studentcreate/',views.StudentCreate.as_view()),
    path('studentRetrive/<int:pk>/',views.StudentRetrive.as_view()),
    path('studentupdate/<int:pk>/',views.StudentUpdate.as_view()),
    path('studentdelete/<int:pk>/',views.StudentDestroy.as_view()),
    # path('studentapi/<int:pk>',views.StudentList.as_view())
]
