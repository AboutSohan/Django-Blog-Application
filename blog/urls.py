from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home_view, name='home'),
    path('<slug:slug>', views.singlePost, name='single'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
