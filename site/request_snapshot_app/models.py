from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class SnapshotRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    SCHEDULE_CHOICES = [
        ('selected_time', 'On Selected Time'),
        ('on_demand', 'On Demand'),
    ]

    # Required fields with appropriate defaults
    vm_name = models.CharField(max_length=255)
    snapshot_name = models.CharField(max_length=255)
    requester = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='snapshot_requests'
    )
    approvers_group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='snapshot_approvals'
    )

    # Optional fields with defaults
    schedule_type = models.CharField(
        max_length=20,
        choices=SCHEDULE_CHOICES,
        default='selected_time'
    )
    scheduled_time = models.DateTimeField(
        null=True,
        blank=True,
        default=None
    )
    include_ram = models.BooleanField(default=False)
    manual_mode = models.BooleanField(default=False)
    reasoning = models.TextField(blank=True, default='')
    
    # Status tracking
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Optional approval tracking
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_snapshots'
    )
    approved_at = models.DateTimeField(
        null=True,
        blank=True,
        default=None
    )
    
    # Optional rejection tracking
    rejected_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='rejected_snapshots'
    )
    rejected_at = models.DateTimeField(
        null=True,
        blank=True,
        default=None
    )
    rejection_reason = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['vm_name']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.vm_name} - {self.snapshot_name} ({self.get_status_display()})"

    def approve(self, user):
        self.status = 'approved'
        self.approved_by = user
        self.approved_at = timezone.now()
        self.save()

    def reject(self, user, reason=''):
        self.status = 'rejected'
        self.rejected_by = user
        self.rejected_at = timezone.now()
        self.rejection_reason = reason
        self.save()

    def complete(self):
        self.status = 'completed'
        self.save()

    def fail(self):
        self.status = 'failed'
        self.save()


class ApproverAction(models.Model):
    ACTION_CHOICES = [
        ('none', 'No Action'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    snapshot_request = models.ForeignKey('SnapshotRequest', on_delete=models.CASCADE, related_name='approver_actions')
    approver = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES, default='none')
    action_time = models.DateTimeField(null=True, blank=True)
    comment = models.TextField(blank=True)

    class Meta:
        unique_together = ['snapshot_request', 'approver']

    def __str__(self):
        return f"{self.approver.username} - {self.action} on {self.snapshot_request}"

@receiver(post_save, sender='request_snapshot_app.SnapshotRequest')
def create_approver_actions(sender, instance, created, **kwargs):
    """Create ApproverAction entries for each user in the approvers group when a new request is created"""
    if created:
        approvers = instance.approvers_group.user_set.all()
        for approver in approvers:
            ApproverAction.objects.create(
                snapshot_request=instance,
                approver=approver,
                action='none'
            )

@receiver(post_save, sender=ApproverAction)
def check_all_approved(sender, instance, **kwargs):
    """Check if all approvers have approved the request"""
    request = instance.snapshot_request
    approver_actions = request.approver_actions.all()
    total_approvers = request.approvers_group.user_set.count()
    
    if total_approvers > 0:
        approved_count = approver_actions.filter(action='approved').count()
        if approved_count == total_approvers:
            request.status = 'approved'
            request.save()
        elif approver_actions.filter(action='rejected').exists():
            request.status = 'rejected'
            request.save()