from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Booking
from django.contrib import messages
from .utils import send_invoice_email

@receiver(post_save, sender=Booking)
def notify_customer(sender, instance, created, **kwargs):
    if not created:
        # If status changed, logic for real-time notification goes here [cite: 35]
        print(f"Notification: Booking for {instance.service.title} is now {instance.status}")

@receiver(post_save, sender=Booking)
def notify_admin_new_booking(sender, instance, created, **kwargs):
    if created:
        # This will show up in the admin messages area
        print(f"NOTIFICATION: New booking received from {instance.customer.username}")

@receiver(pre_save, sender=Booking)
def auto_email_invoice(sender, instance, **kwargs):
    if instance.id:  # Check if this is an update, not a new creation
        try:
            previous = Booking.objects.get(id=instance.id)
            if not previous.is_paid and instance.is_paid:
                send_invoice_email(instance)
        except Booking.DoesNotExist:
            pass