from io import BytesIO
from tempfile import TemporaryDirectory

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from rest_framework.test import APIClient


class ProductImageUploadTests(TestCase):
    def setUp(self):
        self.media_dir = TemporaryDirectory()
        self.addCleanup(self.media_dir.cleanup)
        media_settings = override_settings(MEDIA_ROOT=self.media_dir.name)
        media_settings.enable()
        self.addCleanup(media_settings.disable)

        self.user = User.objects.create_user(username="seller", password="test-password")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def create_image(self, name):
        content = BytesIO()
        Image.new("RGB", (1, 1), color="red").save(content, format="PNG")
        return SimpleUploadedFile(name, content.getvalue(), content_type="image/png")

    def test_create_product_with_multiple_photos(self):
        response = self.client.post(
            reverse("product-list"),
            {
                "name": "Cotton hoodie",
                "sku": "HOODIE-001",
                "price": 3500,
                "stock": 12,
                "images": [
                    self.create_image("front.png"),
                    self.create_image("back.png"),
                ],
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(len(response.data["photos"]), 2)
        self.assertTrue(response.data["photos"][0]["image"].startswith("http"))

    def test_create_product_without_upload_keeps_image_url_support(self):
        response = self.client.post(
            reverse("product-list"),
            {
                "name": "Canvas bag",
                "sku": "BAG-001",
                "price": 1800,
                "stock": 4,
                "image_url": "https://example.com/bag.jpg",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data["image_url"], "https://example.com/bag.jpg")
        self.assertEqual(response.data["photos"], [])
