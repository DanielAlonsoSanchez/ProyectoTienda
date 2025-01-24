from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', views.home, name = 'home'),
]

# Esta línea permite que Django sirva archivos multimedia de 'MEDIA_ROOT' cuando accedas a ellos desde 'MEDIA_URL' mientras desarrollas la aplicación.
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
