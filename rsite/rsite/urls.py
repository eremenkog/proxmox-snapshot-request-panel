"""
URL configuration for rsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
"""
from django.contrib import admin
from django.urls import path, include
from rapp import views
from rapp.functions.manage_requests import manage_request_action


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main, name='main'),
    path('request/', views.request_snapshot, name='request'),
    path('submit-request/', views.submit_request, name='submit_request'),
    path('manage/', views.manage_requests, name='manage'),
    path('manage/<uuid:request_id>/<str:action>/', manage_request_action, name='manage_action'),
    path('actions/', views.actions_history, name='actions'),
]