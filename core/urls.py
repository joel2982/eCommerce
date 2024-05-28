from django.urls import path
from core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name = 'index'),
    path('add_product', views.add_product, name = 'add_product'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
