from django.db.models import Q
from rest_framework import filters, viewsets

from .models import Call
from .serializers import CallSerializer


class CallViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CallSerializer

    def get_queryset(self):
        qs = Call.objects.filter(owner=self.request.user)
        search = self.request.query_params.get("search")
        if search:
            qs = qs.filter(
                Q(customer_name__icontains=search) | Q(order_no__icontains=search)
            )
        return qs
