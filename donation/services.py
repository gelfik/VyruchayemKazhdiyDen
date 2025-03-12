import logging

from donation.models import PromoDonation
from core.services.common_services import object_create, object_exist

logger = logging.getLogger(__name__)


def create_new_promo_donation(order_id: int, **kwargs):
    """Создать новое пожертвование"""

    if not object_exist(PromoDonation.objects, order_id=order_id):
        object_create(PromoDonation, full_check=True, order_id=order_id, **kwargs)
        return
    logger.warning(f"Failed to create promo donation for existing donation with order ID {order_id}")
