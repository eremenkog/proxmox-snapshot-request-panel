from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User


class SnapshotRequest(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    vm_name = models.CharField(max_length=255)
    snapshot_name = models.CharField(max_length=255)
    include_ram = models.BooleanField(default=False)
    reasoning = models.TextField()
    date_time = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default='Active')
    substatus = models.CharField(max_length=50, default='Pending Approval')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'rapp_snapshotrequest'

    def __str__(self):
        return self.vm_name
    
class ApproveList(models.Model):
    scheme_name = models.CharField(max_length=255)
    id = models.CharField(max_length=255, primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    approvers = models.TextField()

    class Meta:
        db_table = 'rapp_approvelist'

