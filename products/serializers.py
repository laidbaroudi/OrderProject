from rest_framework import serializers

from .models import Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "created_at"]
        read_only_fields = ["id", "created_at"]


class ProductSerializer(serializers.ModelSerializer):
    stock_status = serializers.ReadOnlyField()
    photos = ProductImageSerializer(many=True, read_only=True)
    images = serializers.ListField(
        child=serializers.ImageField(),
        required=False,
        write_only=True,
        max_length=5,
    )

    class Meta:
        model = Product
        fields = [
            "id", "name", "category", "price", "stock", "low_stock_threshold",
            "sku", "sold_30d", "description", "image_url", "ai_added",
            "garment_chest_cm", "garment_waist_cm", "follow",
            "expected_restock", "supplier_note", "verified_buyers",
            "created_at", "stock_status", "photos", "images",
        ]
        read_only_fields = ["id", "created_at", "stock_status"]

    def validate_images(self, images):
        max_size = 10 * 1024 * 1024
        if any(image.size > max_size for image in images):
            raise serializers.ValidationError("Each photo must be 10 MB or smaller.")
        return images

    def create(self, validated_data):
        images = validated_data.pop("images", [])
        product = super().create(validated_data)
        for image in images:
            ProductImage.objects.create(product=product, image=image)
        return product

    def update(self, instance, validated_data):
        images = validated_data.pop("images", [])
        product = super().update(instance, validated_data)
        for image in images:
            ProductImage.objects.create(product=product, image=image)
        return product
