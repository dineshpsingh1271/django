from rest_framework import serializers
from .models import HistoricalPerformance, Vendor,PurchaseOrder
from django.shortcuts import get_object_or_404

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'
    def validate_on_time_delivery_rate(self, value):
        """
        Validate that the on-time delivery rate is between 0 and 100.
        """
        if not 0 <= value <= 100:
            raise serializers.ValidationError("On-time delivery rate must be between 0 and 100.")
        return value

    def validate_quality_rating_avg(self, value):
        """
        Validate that the quality rating average is between 0 and 10.
        """
        if not 0 <= value <= 10:
            raise serializers.ValidationError("Quality rating average must be between 0 and 10.")
        return value

    def validate_average_response_time(self, value):
        """
        Validate that the average response time is a positive value.
        """
        if value < 0:
            raise serializers.ValidationError("Average response time must be a positive value.")
        return value

    def validate_fulfillment_rate(self, value):
        """
        Validate that the fulfillment rate is between 0 and 100.
        """
        if not 0 <= value <= 100:
            raise serializers.ValidationError("Fulfillment rate must be between 0 and 100.")
        return value        
class PurchaseOrderSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer(read_only=True)  # Serialize the entire vendor object

    class Meta:
        model = PurchaseOrder
        fields = '__all__'        

    def create(self, validated_data):
        """
        Create and return a new PurchaseOrder instance, given the validated data.
        """        
        vendor_id = validated_data.pop('vendor')
        vendor_instance = get_object_or_404(Vendor, pk=vendor_id)
        validated_data['vendor'] = vendor_instance
        purchase_order_instance = PurchaseOrder.objects.create(**validated_data)
        return purchase_order_instance    
    def to_internal_value(self, data):
        """
        Transform the incoming primitive data into a dictionary of native Python datatypes.
        """        
        return data      
    
    def is_valid(self, raise_exception=False):
        """
        Check if the serializer's fields are valid.
        """        
        valid = super().is_valid(raise_exception=raise_exception)
        return valid    
    
    def validate_order_date(self, value):
        """
        Validate that the order date is not in the past.
        """
        if value < self.context['request'].user.last_login:
            raise serializers.ValidationError("Order date cannot be in the past.")
        return value

    def validate_delivery_date(self, value):
        """
        Validate that the delivery date is after the order date.
        """
        order_date = self.initial_data.get('order_date')
        if order_date and value <= order_date:
            raise serializers.ValidationError("Delivery date must be after the order date.")
        return value

    def validate_quantity(self, value):
        """
        Validate that the quantity is a positive value.
        """
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive value.")
        return value

    def validate_status(self, value):
        """
        Validate that the status is one of the allowed choices.
        """
        if value not in dict(PurchaseOrder.STATUS_CHOICES).keys():
            raise serializers.ValidationError("Invalid status. Choose from 'pending', 'completed', or 'canceled'.")
        return value

    def validate_quality_rating(self, value):
        """
        Validate that the quality rating is between 0 and 10.
        """
        if not (value is None or 0 <= value <= 10):
            raise serializers.ValidationError("Quality rating must be between 0 and 10.")
        return value    

class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id',  'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']

    def validate_on_time_delivery_rate(self, value):
        """
        Validate that the on-time delivery rate is between 0 and 100.
        """
        if not 0 <= value <= 100:
            raise serializers.ValidationError("On-time delivery rate must be between 0 and 100.")
        return value

    def validate_quality_rating_avg(self, value):
        """
        Validate that the quality rating average is between 0 and 10.
        """
        if not 0 <= value <= 10:
            raise serializers.ValidationError("Quality rating average must be between 0 and 10.")
        return value

    def validate_average_response_time(self, value):
        """
        Validate that the average response time is a positive value.
        """
        if value < 0:
            raise serializers.ValidationError("Average response time must be a positive value.")
        return value

    def validate_fulfillment_rate(self, value):
        """
        Validate that the fulfillment rate is between 0 and 100.
        """
        if not 0 <= value <= 100:
            raise serializers.ValidationError("Fulfillment rate must be between 0 and 100.")
        return value
