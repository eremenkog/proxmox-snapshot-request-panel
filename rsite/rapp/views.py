from django.shortcuts import render
from rapp.functions.proxmox import get_all_vms
from rapp.functions.manage_requests import get_snapshot_requests
from rapp.functions.request_snapshot import submit_request
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def main(request):
    return render(request, 'rapp/main.html', {'no_show_back_button': True})

@login_required
def request_snapshot(request):
    vms = sorted(get_all_vms(), key=lambda d: d['name'])
    return render(request, 'rapp/request.html', {'vms': vms})

@login_required
def actions_history(request):
    return render(request, 'rapp/actions.html')

@login_required
def manage_requests(request):
    requests = get_snapshot_requests('Active')
    return render(request, 'rapp/manage.html', {'requests': requests})

def logout_view(request):
    logout(request)
    return redirect('admin:login')