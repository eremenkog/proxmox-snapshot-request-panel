from django.dispatch import receiver
from django_auth_ldap.backend import populate_user

@receiver(populate_user)
def set_staff_status(sender, user, ldap_user, **kwargs):
    user.is_staff = True
    user.save()