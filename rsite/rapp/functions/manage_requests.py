import os
import json
from django.conf import settings
from django.shortcuts import redirect, render
from django.http import HttpResponse
from rapp.models import SnapshotRequest  # Make sure this import matches your model import

def get_snapshot_requests(status_filter=None):
    if status_filter:
        snapshot_requests = SnapshotRequest.objects.filter(status=status_filter)
    else:
        snapshot_requests = SnapshotRequest.objects.all()
    
    return snapshot_requests

def manage_request_action(request, request_id, action):
    try:
        snapshot_request = SnapshotRequest.objects.get(id=request_id)
    except SnapshotRequest.DoesNotExist:
        return HttpResponse("Request not found", status=404)

    if action == 'approve':
        snapshot_request.substatus = 'Approved'
    elif action == 'decline':
        snapshot_request.status = 'Closed'
        snapshot_request.substatus = 'Declined'
    elif action == 'delete':
        snapshot_request.status = 'Closed'
        snapshot_request.substatus = 'Deleted'
    else:
        return HttpResponse("Invalid action", status=400)

    snapshot_request.save()
    return redirect('manage')

def manage_requests_view(request):
    status_filter = request.GET.get('status', None)
    snapshot_requests = get_snapshot_requests(status_filter)
    
    return render(request, 'rapp/manage.html', {
        'snapshot_requests': snapshot_requests
    })
