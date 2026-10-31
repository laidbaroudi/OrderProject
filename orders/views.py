from django.db.models import Q
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["order_no", "total_price", "created_at"]

    def get_queryset(self):
        qs = Order.objects.filter(owner=self.request.user)
        status_param = self.request.query_params.get("status")
        if status_param:
            qs = qs.filter(status=status_param.lower())
        search = self.request.query_params.get("search")
        if search:
            qs = qs.filter(
                Q(customer_name__icontains=search)
                | Q(item_name__icontains=search)
                | Q(order_no__icontains=search)
            )
        return qs

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def _set_status(self, request, pk, new_status, extra=None):
        order = self.get_object()
        order.status = new_status
        if extra:
            for key, val in extra.items():
                setattr(order, key, val)
        order.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        return self._set_status(request, pk, Order.Status.APPROVAL, {"reviewed_by": request.data.get("reviewed_by", "")})

    @action(detail=True, methods=["post"])
    def hold(self, request, pk=None):
        return self._set_status(request, pk, Order.Status.PENDING)

    @action(detail=True, methods=["post"])
    def release(self, request, pk=None):
        return self._set_status(
            request, pk, Order.Status.PACKING,
            {"release_note": request.data.get("release_note", ""), "reviewed_by": request.data.get("reviewed_by", "")},
        )

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        return self._set_status(request, pk, Order.Status.CANCELLED)
