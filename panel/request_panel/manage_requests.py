import os, json
from django.conf import settings
from django.shortcuts import redirect
from django.conf import settings
from django.http import HttpResponse


def get_snapshot_requests():
    directory = os.path.join(settings.BASE_DIR, 'request_panel', 'snapshot_requests')
    snapshot_requests = []

    # Iterate through files in the directory and read JSON data
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as f:
                snapshot_requests.append(json.load(f))
    
    return snapshot_requests

def get_request_file_path(request_id):
    directory = os.path.join(settings.BASE_DIR, 'request_panel', 'snapshot_requests')
    file_path = os.path.join(directory, f"snapshot_request_{request_id}.json")
    return file_path

def manage_request_action(request, request_id, action):
    file_path = get_request_file_path(request_id)

    # Load the snapshot request from the file
    if not os.path.exists(file_path):
        return HttpResponse("Request not found", status=404)

    with open(file_path, 'r') as f:
        snapshot_request = json.load(f)

    # Perform the action
    if action == 'approve':
        snapshot_request['status'] = 'Approved'
    elif action == 'decline':
        snapshot_request['status'] = 'Declined'
    elif action == 'delete':
        os.remove(file_path)
        return redirect('manage_requests')

    # Save the updated snapshot request back to the file
    with open(file_path, 'w') as f:
        json.dump(snapshot_request, f)

    return redirect('manage_requests')
