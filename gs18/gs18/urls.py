from django.contrib import admin
from django.urls import path,include
from api import views
from rest_framework.routers import DefaultRouter

#Creating Router Object
router=DefaultRouter()

#Register StudentViewSet with Router
router.register('studentapi',views.StudentModelViewSet
,basename='student')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls))
]
