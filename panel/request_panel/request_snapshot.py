import os, json, uuid
from datetime import datetime
from django.shortcuts import redirect
from django.conf import settings

def submit_request(request):
    if request.method == 'POST':
        data = {
            'id': str(uuid.uuid4()),
            'vm_name': request.POST.get('vm_name'),
            'snapshot_name': request.POST.get('snapshot_name'),
            'include_ram': request.POST.get('include_ram', False),
            'reasoning': request.POST.get('reasoning'),
            'date_time': request.POST.get('date_time'),
        }
        
        # Handle the form data here (e.g., save to database, send email)
        save_snapshot_request(data)

        return redirect('manage_requests')
    return redirect('request_snapshot')

def save_snapshot_request(data):
    directory = os.path.join(settings.BASE_DIR, 'request_panel', 'snapshot_requests')
    os.makedirs(directory, exist_ok=True)

    filename = f"snapshot_request_{data['id']}.json"
    file_path = os.path.join(directory, filename)

    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

    return file_path