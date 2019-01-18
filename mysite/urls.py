"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

    Lines between triple quotes are called docstrings – you can write them at the top of a file, class or method to describe what it does. They won't be run by Python.
"""
from django.contrib import admin
from django.urls import path, include #we are using the include function

#we will import URLs from our blog application to the main mysite/urls.py file.

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')), #Django will now redirect everything that comes into 'http://127.0.0.1:8000/' to blog.urls and looks for further instructions there.
]
