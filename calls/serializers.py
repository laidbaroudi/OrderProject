from rest_framework import serializers

from .models import Call


class CallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Call
        fields = [
            "id", "order", "customer_name", "order_no", "status",
            "duration_sec", "sentiment", "transcript", "created_at",
        ]
        read_only_fields = ["id", "created_at"]
