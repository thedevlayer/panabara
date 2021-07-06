from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
# from examples import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('examples.urls')),
]
