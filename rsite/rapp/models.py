from django.db import models
from django.dispatch import receiver


class SnapshotRequest(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    vm_name = models.CharField(max_length=255)
    snapshot_name = models.CharField(max_length=255)
    include_ram = models.BooleanField(default=False)
    reasoning = models.TextField()
    date_time = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default='Active')
    substatus = models.CharField(max_length=50, default='Pending Approval')

    class Meta:
        db_table = 'snapshots'

    def __str__(self):
        return self.vm_name