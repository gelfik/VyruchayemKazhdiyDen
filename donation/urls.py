from django.urls import include, path
from rest_framework.routers import DefaultRouter

from donation.views import (
    PromoDonationWebhookViewSet,
    PublicPromoDonationViewSet,
)

app_name = "donation"
router = DefaultRouter()

router.register(
    "promo_donation/webhook",
    PromoDonationWebhookViewSet,
    basename="promo-donation-webhooks",
)
router.register(
    "promo_donation/public",
    PublicPromoDonationViewSet,
    basename="promo-donation-public",
)
urlpatterns = [
    path("", include(router.urls)),
]
