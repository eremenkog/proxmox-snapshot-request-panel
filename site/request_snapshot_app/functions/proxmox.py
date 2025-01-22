import requests
from request_snapshot.secrets import PROXMOX_URL, PROXMOX_USER, PROXMOX_PASSWORD, PROXMOX_NODE_NAME

def get_proxmox_auth_token():
    url = f"{PROXMOX_URL}/access/ticket"
    data = {
        'username': PROXMOX_USER,
        'password': PROXMOX_PASSWORD
    }
    
    response = requests.post(url, data=data, verify=False)  # Disable SSL verification for this example
    response.raise_for_status()                             # Raise an error for bad responses
    json_response = response.json()
    
    return {
        'ticket': json_response['data']['ticket'],
        'csrf_token': json_response['data']['CSRFPreventionToken']
    }

def get_all_vms():
    tokens = get_proxmox_auth_token()
    ticket = tokens['ticket']
    csrf_token = tokens['csrf_token']

    headers = {
        'CSRFPreventionToken': csrf_token,
        'Cookie': f"PVEAuthCookie={ticket}"
    }

    url = f"{PROXMOX_URL}/nodes/{PROXMOX_NODE_NAME}/qemu"

    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()

    vms = [entry for entry in response.json()['data'] if entry.get('template') != 1]

    # Fetch snapshots for each VM
    for vm in vms:
        vm_id = vm['vmid']
        snapshot_url = f"{PROXMOX_URL}/nodes/{PROXMOX_NODE_NAME}/qemu/{vm_id}/snapshot"
        snapshot_response = requests.get(snapshot_url, headers=headers, verify=False)
        if snapshot_response.status_code == 200:
            vm['snapshots'] = snapshot_response.json()['data']
        else:
            vm['snapshots'] = []
    return vms

def create_snapshot(vm_name, snapshot_name, description=""):
    vms = get_all_vms()
    vm = next((vm for vm in vms if vm['name'] == vm_name), None)

    if not vm:
        raise ValueError(f"VM with name '{vm_name}' not found.")

    vm_id = vm['vmid']

    tokens = get_proxmox_auth_token()
    ticket = tokens['ticket']
    csrf_token = tokens['csrf_token']

    headers = {
        'CSRFPreventionToken': csrf_token,
        'Cookie': f"PVEAuthCookie={ticket}"
    }

    url = f"{PROXMOX_URL}/nodes/{PROXMOX_NODE_NAME}/qemu/{vm_id}/snapshot"

    snapshot_data = {
        "snapname": snapshot_name,
        "description": description,
    }

    try:
        response = requests.post(url, headers=headers, data=snapshot_data, verify=False)
        response.raise_for_status()

        print(f"Snapshot '{snapshot_name}' created successfully for VM '{vm_name}' (ID: {vm_id}) on node {PROXMOX_NODE_NAME}.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to create snapshot: {e}")
        raise

def delete_snapshot(vm_name, snapshot_name):
    vms = get_all_vms()
    vm = next((vm for vm in vms if vm['name'] == vm_name), None)

    if not vm:
        raise ValueError(f"VM with name '{vm_name}' not found.")

    vm_id = vm['vmid']

    tokens = get_proxmox_auth_token()
    ticket = tokens['ticket']
    csrf_token = tokens['csrf_token']

    headers = {
        'CSRFPreventionToken': csrf_token,
        'Cookie': f"PVEAuthCookie={ticket}"
    }

    url = f"{PROXMOX_URL}/nodes/{PROXMOX_NODE_NAME}/qemu/{vm_id}/snapshot/{snapshot_name}"

    try:
        response = requests.delete(url, headers=headers, verify=False)
        response.raise_for_status()

        print(f"Snapshot '{snapshot_name}' deleted successfully for VM '{vm_name}' (ID: {vm_id}) on node {PROXMOX_NODE_NAME}.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to delete snapshot: {e}")
        raise

def rollback_snapshot(vm_name, snapshot_name):
    vms = get_all_vms()
    vm = next((vm for vm in vms if vm['name'] == vm_name), None)

    if not vm:
        raise ValueError(f"VM with name '{vm_name}' not found.")

    vm_id = vm['vmid']

    tokens = get_proxmox_auth_token()
    ticket = tokens['ticket']
    csrf_token = tokens['csrf_token']

    headers = {
        'CSRFPreventionToken': csrf_token,
        'Cookie': f"PVEAuthCookie={ticket}"
    }

    url = f"{PROXMOX_URL}/nodes/{PROXMOX_NODE_NAME}/qemu/{vm_id}/snapshot/{snapshot_name}/rollback"

    snapshot_data = {
        "snapname": snapshot_name,
        "start": "0",
    }

    try:
        response = requests.post(url, headers=headers, data=snapshot_data, verify=False)
        response.raise_for_status()

        print(f"VM '{vm_name}' (ID: {vm_id}) on node {PROXMOX_NODE_NAME} rolled back successfully to snapshot '{snapshot_name}'.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to rollback snapshot: {e}")
        raise

    # POST /api2/json/nodes/{node}/qemu/{vmid}/snapshot/{snapname}/rollback