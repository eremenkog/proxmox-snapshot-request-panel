from django.shortcuts import render
from rapp.functions.proxmox import get_all_vms
from rapp.functions.manage_requests import get_snapshot_requests
from rapp.functions.request_snapshot import submit_request

def main(request):
    return render(request, 'rapp/main.html')

def request_snapshot(request):
    vms = get_all_vms()
    return render(request, 'rapp/request.html', {'vms': vms})

def actions_history(request):
    return render(request, 'rapp/actions.html')

def manage_requests(request):
    requests = get_snapshot_requests('Active')
    return render(request, 'rapp/manage.html', {'requests': requests})
