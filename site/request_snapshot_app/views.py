from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from request_snapshot_app.functions.proxmox import get_all_vms
from .functions.proxmox import create_snapshot as create_proxmox_snapshot
from .functions.proxmox import delete_snapshot as delete_proxmox_snapshot
from .functions.proxmox import rollback_snapshot as rollback_proxmox_snapshot
from django.contrib.auth.models import Group
from .models import SnapshotRequest, ApproverAction
from django.contrib import messages
from datetime import datetime
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST


@login_required
def main(request):
    return render(request, 'request_snapshot_app/main.html', {'no_show_back_button': True})

def logout_view(request):
    logout(request)
    return redirect('admin:login')

@login_required
def request_snapshot(request):
    vms = sorted(get_all_vms(), key=lambda d: d['name'])
    groups = Group.objects.all()
    return render(request, 'request_snapshot_app/request.html', {'vms': vms, 'groups': groups})

@login_required
def submit_request(request):
    if request.method != 'POST':
        return redirect('request')
    
    try:
        # Extract form data
        vm_name = request.POST.get('vm_name')
        snapshot_name = request.POST.get('snapshot_name')
        schedule_type = request.POST.get('schedule')
        scheduled_time_str = request.POST.get('date_time')
        include_ram = request.POST.get('include_ram') == 'on'
        manual_mode = request.POST.get('manual') == 'on'
        approvers_group_id = request.POST.get('group')
        reasoning = request.POST.get('reasoning', '')

        # Convert scheduled time string to datetime if needed
        scheduled_time = None
        if schedule_type == 'selected_time' and scheduled_time_str:
            try:
                scheduled_time = datetime.strptime(scheduled_time_str, '%d/%m/%Y %H:%M')
            except ValueError:
                messages.error(request, 'Invalid date/time format')
                return redirect('request')

        # Create snapshot request
        snapshot_request = SnapshotRequest.objects.create(
            vm_name=vm_name,
            snapshot_name=snapshot_name,
            schedule_type=schedule_type,
            scheduled_time=scheduled_time,
            include_ram=include_ram,
            manual_mode=manual_mode,
            reasoning=reasoning,
            requester=request.user,
            approvers_group_id=approvers_group_id
        )

        messages.success(request, 'Snapshot request submitted successfully')
        return redirect('main')

    except Exception as e:
        messages.error(request, f'Error submitting request: {str(e)}')
        return redirect('request')

@login_required
@require_POST
def approve_request(request, request_id):
    snapshot_request = get_object_or_404(SnapshotRequest, id=request_id)
    
    # Check if user is in approvers group
    if request.user not in snapshot_request.approvers_group.user_set.all():
        return JsonResponse({'error': 'Not authorized'}, status=403)
    
    try:
        approver_action = ApproverAction.objects.get(
            snapshot_request=snapshot_request,
            approver=request.user
        )
        approver_action.action = 'approved'
        approver_action.action_time = timezone.now()
        approver_action.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Request approved successfully'
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)

@login_required
@require_POST
def reject_request(request, request_id):
    snapshot_request = get_object_or_404(SnapshotRequest, id=request_id)
    
    # Check if user is in approvers group
    if request.user not in snapshot_request.approvers_group.user_set.all():
        return JsonResponse({'error': 'Not authorized'}, status=403)
    
    try:
        approver_action = ApproverAction.objects.get(
            snapshot_request=snapshot_request,
            approver=request.user
        )
        approver_action.action = 'rejected'
        approver_action.action_time = timezone.now()
        approver_action.comment = request.POST.get('reason', '')
        approver_action.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Request rejected successfully'
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)

@login_required
@require_POST
def delete_request(request, request_id):
    snapshot_request = get_object_or_404(SnapshotRequest, id=request_id)
    
    # Check if user is the requester
    if request.user != snapshot_request.requester:
        return JsonResponse({'error': 'Not authorized'}, status=403)
    
    try:
        snapshot_request.delete()
        return JsonResponse({
            'status': 'success',
            'message': 'Request deleted successfully'
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)

@login_required
@require_POST
def complete_request(request, request_id):
    snapshot_request = get_object_or_404(SnapshotRequest, id=request_id)
    
    # Check if user is the requester
    if request.user != snapshot_request.requester:
        return JsonResponse({'error': 'Not authorized'}, status=403)
    
    try:
        # Mark the request as completed
        snapshot_request.complete()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Request completed successfully'
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)

@login_required
def manage_requests(request):
    # Get filter parameters
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', 'all')
    date_filter = request.GET.get('date_filter', 'all')

    # Start with all requests
    snapshot_requests = SnapshotRequest.objects.prefetch_related(
        'approver_actions__approver'
    ).select_related('requester')

    # Apply filters
    if search_query:
        snapshot_requests = snapshot_requests.filter(
            Q(vm_name__icontains=search_query) |
            Q(snapshot_name__icontains=search_query) |
            Q(requester__username__icontains=search_query)
        )

    if status_filter != 'all':
        snapshot_requests = snapshot_requests.filter(status=status_filter)

    if date_filter != 'all':
        today = timezone.now().date()
        if date_filter == 'today':
            snapshot_requests = snapshot_requests.filter(created_at__date=today)
        elif date_filter == 'week':
            snapshot_requests = snapshot_requests.filter(
                created_at__date__gte=today - timezone.timedelta(days=7)
            )
        elif date_filter == 'month':
            snapshot_requests = snapshot_requests.filter(
                created_at__date__gte=today - timezone.timedelta(days=30)
            )

    # Prepare data for template
    requests_data = []
    for snapshot_request in snapshot_requests:
        approvers = snapshot_request.approver_actions.all()
        
        approvers_with_decisions = [
            {
                'username': action.approver.username,
                'decision': action.action if action.action != 'none' else 'none',
            }
            for action in approvers
        ]
        
        requests_data.append({
            'id': snapshot_request.id,
            'vm_name': snapshot_request.vm_name,
            'snapshot_name': snapshot_request.snapshot_name,
            'requester': snapshot_request.requester,
            'schedule_type': snapshot_request.schedule_type,
            'scheduled_time': snapshot_request.scheduled_time,
            'manual_mode': snapshot_request.manual_mode,
            'status': snapshot_request.status,
            'created_at': snapshot_request.created_at,
            'approvers': approvers_with_decisions,
            'reasoning': snapshot_request.reasoning,
        })

    status_choices = [choice for choice in SnapshotRequest.STATUS_CHOICES]

    return render(request, 'request_snapshot_app/manage.html', {
        'requests': requests_data,
        'status_choices': status_choices,
        'search_query': search_query,
        'status_filter': status_filter,
        'date_filter': date_filter,
    })


@login_required
def actions(request):
    approved_requests = SnapshotRequest.objects.filter(status='approved').select_related('requester')
    vms = sorted(get_all_vms(), key=lambda d: d['name'])

    for vm in vms:
        for snapshot in (vm['snapshots']):
            if snapshot.get('snaptime'):
                snapshot['snaptime'] = datetime.fromtimestamp(snapshot['snaptime'])

    requests_data = []
    for snapshot_request in approved_requests:
        requests_data.append({
            'id': snapshot_request.id,
            'vm_name': snapshot_request.vm_name,
            'snapshot_name': snapshot_request.snapshot_name,
            'requester': snapshot_request.requester,
            'schedule_type': snapshot_request.schedule_type,
            'scheduled_time': snapshot_request.scheduled_time,
            'manual_mode': snapshot_request.manual_mode,
            'created_at': snapshot_request.created_at,
            'reasoning': snapshot_request.reasoning,  # Include reasoning here
        })

    return render(request, 'request_snapshot_app/actions.html', {
        'approved_requests': requests_data,
        'vms': vms,
    })

@require_POST
def create_snapshot(request):
    import json
    data = json.loads(request.body)
    vm_name = data.get('vm_name')
    snapshot_name = data.get('snapshot_name')
    description = data.get('description', '')

    try:
        # Call the Proxmox function to create the snapshot
        create_proxmox_snapshot(vm_name, snapshot_name, description)
        return JsonResponse({
            'success': True,
            'message': f"Snapshot '{snapshot_name}' created successfully for VM '{vm_name}' and description '{description}'.",
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f"Failed to create snapshot: {str(e)}",
        }, status=500)
    
@require_POST
def delete_snapshot(request):
    import json
    data = json.loads(request.body)
    vm_name = data.get('vm_name')
    snapshot_name = data.get('snapshot_name')

    try:
        # Call the Proxmox function to create the snapshot
        delete_proxmox_snapshot(vm_name, snapshot_name)
        return JsonResponse({
            'success': True,
            'message': f"Snapshot '{snapshot_name}' deleted successfully for VM '{vm_name}'.",
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f"Failed to delete snapshot: {str(e)}",
        }, status=500)

@require_POST
def rollback_snapshot(request):
    import json
    data = json.loads(request.body)
    vm_name = data.get('vm_name')
    snapshot_name = data.get('snapshot_name')

    try:
        # Call the Proxmox function to create the snapshot
        rollback_proxmox_snapshot(vm_name, snapshot_name)
        return JsonResponse({
            'success': True,
            'message': f"VM '{vm_name}' rolled back to snapshot '{snapshot_name}' successfully.",
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f"Failed to rollback to snapshot: {str(e)}",
        }, status=500)