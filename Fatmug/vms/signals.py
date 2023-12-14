# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.db.models import Avg, F
from django.utils import timezone
import pytz
from datetime import datetime
from .models import PurchaseOrder

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_performance(sender, instance, **kwargs):
    """
    Signal handler to update vendor performance metrics when a purchase order is saved.
    
    Triggered on post-save.
    Updates on_time_delivery_rate, quality_rating_avg, average_response_time, and fulfillment_rate.
    Metrics are based on completed purchase orders.
    """
    vendor = instance.vendor
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    
    if completed_orders.count() == 0:
        # Avoid division by zero when there are no completed orders.
        vendor.on_time_delivery_rate = 0
        vendor.quality_rating_avg = 0
        vendor.average_response_time = 0
        vendor.fulfillment_rate = 0
    else:
        utc_timezone = settings.TIME_ZONE if settings.USE_TZ else timezone.utc
        ist_timezone = pytz.timezone(utc_timezone)
        # Get the current datetime in the specified timezone.
        current_datetime = datetime.now(ist_timezone)    

        # On-Time Delivery Rate
        on_time_deliveries = completed_orders.filter(delivery_date__lte=current_datetime)
        vendor.on_time_delivery_rate = (on_time_deliveries.count() / completed_orders.count()) * 100

        # Quality Rating Average
        quality_ratings = completed_orders.exclude(quality_rating__isnull=True)
        vendor.quality_rating_avg = quality_ratings.aggregate(Avg('quality_rating'))['quality_rating__avg'] if quality_ratings.exists() else 0

        # Average Response Time
        response_times = completed_orders.exclude(acknowledgment_date__isnull=True)
        vendor.average_response_time = response_times.aggregate(Avg(F('acknowledgment_date') - F('issue_date')))['acknowledgment_date__avg'] if response_times.exists() else 0

        # Fulfilment Rate
        fulfilled_orders = completed_orders.exclude(status='canceled')
        vendor.fulfillment_rate = (fulfilled_orders.count() / completed_orders.count()) * 100

    vendor.save()

