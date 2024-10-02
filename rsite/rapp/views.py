from django.shortcuts import render, redirect, get_object_or_404
from rapp.functions.proxmox import get_all_vms
from rapp.functions.manage_requests import get_snapshot_requests
from rapp.functions.request_snapshot import submit_request
from rapp.functions.manage_schemes import get_schemes
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from rapp.models import ApproveList
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST


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

@login_required
def schemes(request):
    schemes = ApproveList.objects.all()
    return render(request, 'rapp/schemes.html', {'schemes': schemes})

@login_required
@require_POST
def delete_scheme(request, scheme_id):
    scheme = get_object_or_404(ApproveList, id=scheme_id)
    scheme.delete()
    return redirect('schemes')

import uuid
@login_required
def create_scheme(request):
    if request.method == 'POST':
        scheme_name = request.POST.get('scheme_name')
        approvers = request.POST.get('approvers')
        new_scheme = ApproveList(
            id=str(uuid.uuid4()),
            scheme_name=scheme_name,
            approvers=approvers,
            author=request.user
        )
        new_scheme.save()
        return redirect('schemes')
    return redirect('schemes')

def logout_view(request):
    logout(request)
    return redirect('admin:login')