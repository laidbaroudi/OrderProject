from rest_framework import viewsets

from .models import FitCheck
from .serializers import FitCheckSerializer


class FitCheckViewSet(viewsets.ModelViewSet):
    serializer_class = FitCheckSerializer
    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):
        qs = FitCheck.objects.filter(owner=self.request.user)
        product = self.request.query_params.get("product")
        if product:
            qs = qs.filter(product_id=product)
        return qs

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
