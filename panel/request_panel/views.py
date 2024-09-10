from django.shortcuts import render
from .proxmox import get_all_vms
from .request_snapshot import submit_request
from .manage_requests import get_snapshot_requests, manage_request_action


def selector(request):
    return render(request, 'request_panel/selector.html')

def request_snapshot(request):
    vms = get_all_vms()
    return render(request, 'request_panel/request_snapshot.html', {'vms': vms})

def actions_history(request):
    return render(request, 'request_panel/actions_history.html')

def manage_requests(request):
    return render(request, 'request_panel/manage_requests.html')

def manage_requests(request):
    requests = get_snapshot_requests('Active')
    return render(request, 'request_panel/manage_requests.html', {'requests': requests})
