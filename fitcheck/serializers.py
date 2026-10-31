from rest_framework import serializers

from products.models import Product

from .models import FitCheck


class FitCheckSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        source="product", queryset=Product.objects.all()
    )

    class Meta:
        model = FitCheck
        fields = ["id", "product_id", "score", "verdict", "created_at"]
        read_only_fields = ["id", "created_at"]
