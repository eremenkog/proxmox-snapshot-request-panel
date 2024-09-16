import uuid
from django.shortcuts import redirect
from django.conf import settings
from rapp.models import SnapshotRequest

def submit_request(request):
    if request.method == 'POST':
        snapshot_id = str(uuid.uuid4())
        vm_name = request.POST.get('vm_name')
        snapshot_name = request.POST.get('snapshot_name')
        include_ram = request.POST.get('include_ram', False) == 'on'  # Checkbox check
        reasoning = request.POST.get('reasoning')
        date_time = request.POST.get('date_time')
        
        # Handle the form data here (e.g., save to database, send email)
        save_snapshot_request(snapshot_id, vm_name, snapshot_name, include_ram, reasoning, date_time)

        return redirect('request')
    return redirect('request')

def save_snapshot_request(snapshot_id, vm_name, snapshot_name, include_ram, reasoning, date_time):
    SnapshotRequest.objects.create(
        id=snapshot_id,
        vm_name=vm_name,
        snapshot_name=snapshot_name,
        include_ram=include_ram,
        reasoning=reasoning,
        date_time=date_time,
        status="Active",
        substatus="Pending Approval"
    )

