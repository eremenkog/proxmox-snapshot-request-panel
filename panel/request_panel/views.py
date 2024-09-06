from django.shortcuts import render, redirect
from .proxmox import get_all_vms

def selector(request):
    return render(request, 'request_panel/selector.html')

def request_snapshot(request):
    all_vms = get_all_vms()
    vms = sorted(vm['name'] for vm in all_vms)
    return render(request, 'request_panel/request_snapshot.html', {'vms': vms})

def manage_requests(request):
    return render(request, 'request_panel/manage_requests.html')

def actions_history(request):
    return render(request, 'request_panel/actions_history.html')

def submit_request(request):
    if request.method == 'POST':
        vm_name = request.POST.get('vm_name')
        snapshot_name = request.POST.get('snapshot_name')
        include_ram = 'include_ram' in request.POST
        reasoning = request.POST.get('reasoning')
        
        # Handle the form data here (e.g., save to database, send email)
        
        return redirect('request_snapshot')  # Redirect to the same page or another page
    return redirect('request_snapshot')
