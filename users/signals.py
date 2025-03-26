from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import CustomUser

def send_email_to_admins(subject, message):
    admins = CustomUser.objects.filter(is_superuser=True).values_list('email', flat=True)
    if admins:
        send_mail(
            subject,
            message,
            'nsardorbek776@gmail.com',
            list(admins),
            fail_silently=False
        )

@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        send_email_to_admins('Hello Admin!', f'{instance.email} created successfully!')
    else:
        send_email_to_admins('User Updated!', f'{instance.email} has been updated.')

@receiver(post_delete, sender=CustomUser)
def delete_profile(sender, instance, **kwargs):
    send_email_to_admins('User Deleted!', f'{instance.email} has been deleted.')
