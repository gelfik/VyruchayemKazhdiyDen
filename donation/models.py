from django.db import models

from core.fields import LowercaseEmailField
from core.mixins.models import CreatedUpdatedMixin


# Create your models here.


class PromoAction(CreatedUpdatedMixin):
    name = models.CharField(verbose_name="Название акции", max_length=255)

    class Meta:
        verbose_name = "Акция"
        verbose_name_plural = "Акции"

    def __str__(self):
        return f"ID: {self.pk} - {self.name}"


class PromoDonation(CreatedUpdatedMixin):
    name = models.CharField(verbose_name="Имя", max_length=100)
    email = LowercaseEmailField(verbose_name="Email")
    order_id = models.IntegerField(verbose_name="ID заказа")
    amount = models.PositiveIntegerField(verbose_name="Сумма")
    promo_action = models.ForeignKey(
        "donation.PromoAction",
        verbose_name="Акция",
        related_name="donations",
        on_delete=models.CASCADE,
        default=None
    )

    class Meta:
        verbose_name = "Пожертвование в промо-акцию"
        verbose_name_plural = "Пожертвование в промо-акции"
        constraints = [
            models.UniqueConstraint(
                fields=["promo_action", "order_id"],
                name="unique_order_per_promo_action"
            )
        ]

    def __str__(self):
        return f"ID: {self.pk} - Акция: {self.promo_action.name if self.promo_action else None}"
