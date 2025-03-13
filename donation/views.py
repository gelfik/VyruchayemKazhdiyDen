from django.db.models import Sum
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from donation.models import PromoDonation
from donation.permissions import WebhookAPIPermission
from donation.serializers import (
    NewPromoDonationWebhookSerializer,
    PublicPromoDonationSerializer,
)
from donation.services import create_new_promo_donation


class PromoDonationWebhookViewSet(viewsets.GenericViewSet):
    permission_classes = (WebhookAPIPermission,)
    throttle_classes = []

    @action(methods=["POST"], detail=False, serializer_class=NewPromoDonationWebhookSerializer)
    def new_donation(self, request, *args, **kwargs):
        """webhook для нового пожертвования в промо акцию"""

        if not request.data.get("test", None):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            create_new_promo_donation(**serializer.cleaned_data)
        return Response(status=status.HTTP_200_OK)


class PublicPromoDonationViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = PublicPromoDonationSerializer
    queryset = PromoDonation.objects.all().order_by("-created")
    pagination_class = None
    throttle_classes = []

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        aggregated_sum = queryset.aggregate(total_amount=Sum("amount")).get("total_amount", 0)
        response_data = aggregated_sum if aggregated_sum else 0
        return Response(data=response_data, status=status.HTTP_200_OK)
