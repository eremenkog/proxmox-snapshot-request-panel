"""
URL configuration for request_snapshot project.

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
from django.urls import path
from request_snapshot_app import views
from request_snapshot_app.views import logout_view, create_snapshot, delete_snapshot, rollback_snapshot

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main, name='main'),
    path('logout/', logout_view, name='logout'),
    path('request/', views.request_snapshot, name='request'),
    path('submit-request/', views.submit_request, name='submit_request'),
    path('manage/', views.manage_requests, name='manage'),
    path('approve-request/<int:request_id>/', views.approve_request, name='approve_request'),
    path('reject-request/<int:request_id>/', views.reject_request, name='reject_request'),
    path('delete-request/<int:request_id>/', views.delete_request, name='delete_request'),
    path('actions/', views.actions, name='actions'),
    path('create-snapshot/', create_snapshot, name='create_snapshot'),
    path('delete-snapshot/', delete_snapshot, name='delete_snapshot'),
    path('rollback-snapshot/', rollback_snapshot, name='rollback_snapshot'),
    path('complete-request/<int:request_id>/', views.complete_request, name='complete_request'),
]
