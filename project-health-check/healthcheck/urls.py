from django.urls import include, path
from rest_framework import routers
from .api import views

router = routers.DefaultRouter()

router.register(r"server", views.ServerHealthLogViewset, basename="System-Health-Log")
router.register(r"agent", views.AgentAuthViewSet, basename="Agent-Access")

urlpatterns = [
    path("", include(router.urls)),
]
