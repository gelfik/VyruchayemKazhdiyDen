from django.db import models

from core.fields import LowercaseEmailField
from core.mixins.models import CreatedUpdatedMixin


# Create your models here.

class PromoDonation(CreatedUpdatedMixin):
    name = models.CharField(verbose_name="Имя", max_length=100)
    email = LowercaseEmailField(verbose_name="Email")
    order_id = models.IntegerField(verbose_name="ID заказа", unique=True)
    amount = models.PositiveIntegerField(verbose_name="Сумма")

    class Meta:
        verbose_name = "Пожертвование в промо-акцию"
        verbose_name_plural = "Пожертвование в промо-акции"
