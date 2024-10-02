from rapp.models import ApproveList
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404

def get_schemes(author_filter=None):
    if author_filter:
        schemes = ApproveList.objects.filter(status=author_filter)
    else:
        schemes = ApproveList.objects.all()
    return schemes

def manage_scheme_action(request, request_id, action):
    scheme = get_object_or_404(ApproveList, id=request_id)

    if action == 'edit':
        #Action to edit
        pass
    elif action == 'delete':
        scheme.delete()
        return redirect('schemes')
    else:
        return HttpResponse("Invalid action", status=400)

    return redirect('schemes')