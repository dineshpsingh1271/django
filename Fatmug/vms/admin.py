from django.contrib import admin



# Register your models here.


from .models import HistoricalPerformance, Vendor, PurchaseOrder


# Register your models here.
@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ["name", "address","contact_details","vendor_code","on_time_delivery_rate","quality_rating_avg","average_response_time","fulfillment_rate"]
    list_filter = ["vendor_code","quality_rating_avg"]

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ["po_number", "vendor","order_date","status","delivery_date","items","quantity","quality_rating","issue_date","acknowledgment_date"]
    list_filter = ["vendor","order_date","delivery_date","issue_date","acknowledgment_date"]

@admin.register(HistoricalPerformance)
class HistoricalPerformanceAdmin(admin.ModelAdmin):
    list_display = [ "vendor","date","on_time_delivery_rate","quality_rating_avg","quality_rating_avg","average_response_time","fulfillment_rate"]
    list_filter = ["vendor","date","quality_rating_avg"]


