from django.urls import path
from .views import selector, request_snapshot, manage_requests, actions_history
from .manage_requests import manage_request_action

urlpatterns = [
    path('selector/', selector, name='selector'),
    path('request-snapshot/', request_snapshot, name='request_snapshot'),
    path('manage-requests/', manage_requests, name='manage_requests'),
    path('manage-requests/<uuid:request_id>/<str:action>/', manage_request_action, name='manage_action'),
    path('actions-history/', actions_history, name='actions_history'),
]