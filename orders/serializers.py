from rest_framework import serializers

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id", "order_no", "customer_name", "customer", "product",
            "item_name", "quantity", "total_price", "status", "source",
            "created_at", "reviewed_by", "release_note",
        ]
        read_only_fields = ["id", "created_at"]
