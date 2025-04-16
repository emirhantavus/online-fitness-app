from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('core.urls')),
    path('api/',include('users.urls')),
    path('api/',include('blog.urls')),
    path('api/',include('subplans.urls')),
    path('api/',include('programs.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
