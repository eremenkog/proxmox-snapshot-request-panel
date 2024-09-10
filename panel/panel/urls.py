from django.contrib import admin
from django.urls import include, path
from request_panel import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('request_panel/', include('request_panel.urls')),
    path('selector/', include('request_panel.urls')),
    path('request-snapshot/', views.request_snapshot, name='request_snapshot'),
    path('submit-request/', views.submit_request, name='submit_request'),
    path('manage-requests/', views.manage_requests, name='manage_requests'),
    path('manage-requests/<int:request_id>/<str:action>/', views.manage_request_action, name='manage_action'),
    path('actions-history/', views.actions_history, name='actions_history'),
]