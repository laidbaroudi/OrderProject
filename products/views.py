from django.db.models import Q
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "category", "sku", "description"]
    ordering_fields = ["name", "price", "stock", "sold_30d", "created_at"]

    def get_queryset(self):
        profile = getattr(self.request.user, "profile", None)
        if profile is not None and profile.role == "customer":
            qs = Product.objects.all()
        else:
            qs = Product.objects.filter(owner=self.request.user)
        category = self.request.query_params.get("category")
        if category:
            qs = qs.filter(category__iexact=category)
        search = self.request.query_params.get("search")
        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(sku__icontains=search))
        return qs

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        status_param = request.query_params.get("status")
        if status_param:
            status_param = status_param.lower()
            items = [p for p in queryset if p.stock_status == status_param]
            serializer = self.get_serializer(items, many=True)
            return Response(serializer.data)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def follow(self, request, pk=None):
        product = self.get_object()
        product.follow = not product.follow
        product.save(update_fields=["follow"])
        return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
