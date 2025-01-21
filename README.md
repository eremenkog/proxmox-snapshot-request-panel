# Proxmox snapshot requests

Django powered site that helps you to create snapshot requests, manage them with custom user groups and create snapshots without direct access to Proxmox management panel.

## Prerequisites

1. Active Directory
2. Proxmox

## Installation
1. Create LDAP BIND account

```bash
AUTH_LDAP_SERVER_URI = "ldap://192.168.192.162"
AUTH_LDAP_BIND_DN = "ldap_bind@lab.domain"
AUTH_LDAP_BIND_PASSWORD = "#######"
AUTH_LDAP_SCOPE = "OU=Lab_Users,DC=lab,DC=domain"
```

2. Create Proxmox account with necessary API access
```bash
PROXMOX_URL = "https://192.168.192.131:8006/api2/json"
PROXMOX_USER = "snapshot@pve"
PROXMOX_PASSWORD = "#######"
PROXMOX_NODE_NAME = "pve"
```

3. Deploy site, providing necessary credentials as variables shown above.

## How to use
