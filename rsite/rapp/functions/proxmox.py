import requests
from rsite.secrets import PROXMOX_URL, PROXMOX_USER, PROXMOX_PASSWORD, PROXMOX_NODE_NAME

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
    
    return response.json()['data']
