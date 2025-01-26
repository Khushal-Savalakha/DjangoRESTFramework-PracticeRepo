from django.contrib import admin
from django.urls import path,include
import api
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('api.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
