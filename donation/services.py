import logging

from core.services.common_services import object_create, object_exist
from donation.models import PromoDonation

logger = logging.getLogger(__name__)


def create_new_promo_donation(order_id: int, promo_action_id: int, **kwargs):
    """Создать новое пожертвование"""

    if not object_exist(PromoDonation.objects, order_id=order_id, promo_action_id=promo_action_id):
        object_create(PromoDonation, full_check=True, order_id=order_id, promo_action_id=promo_action_id, **kwargs)
        return
    logger.warning(
        f"Failed to create promo donation for existing donation with order ID {order_id} Promo action ID {promo_action_id}")
