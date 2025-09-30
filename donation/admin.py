from django.contrib import admin
from django.db.models.aggregates import Sum

from donation.models import PromoDonation, PromoAction


class PromoActionAllFilter(admin.SimpleListFilter):
    title = "Акция"
    parameter_name = "promo_action"

    def lookups(self, request, model_admin):
        return [(str(pa.pk), pa.name) for pa in PromoAction.objects.all()]

    def queryset(self, request, qs):
        v = self.value()
        return qs.filter(promo_action_id=v) if v else qs


# Register your models here.

@admin.register(PromoAction)
class PromoActionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "created",
    )


@admin.register(PromoDonation)
class PromoDonationAdmin(admin.ModelAdmin):
    change_list_template = "admin/donation/change_list_promo_donation.html"
    list_display = (
        "id",
        "email",
        "amount",
        "created",
        "promo_action_field"
    )

    search_fields = ["email", "id"]
    search_help_text = "Поиск по email, id"

    list_filter = (
        PromoActionAllFilter,
    )

    @admin.display(ordering="promo_action__name", description="Акция")
    def promo_action_field(self, obj):
        return obj.promo_action.name if obj.promo_action_id else "-"

    def has_change_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context or {})
        try:
            cl = response.context_data["cl"]  # ChangeList
            qs = cl.queryset  # уже с фильтрами/поиском/ordering
        except (AttributeError, KeyError):
            return response

        total = qs.aggregate(total_amount=Sum("amount"))["total_amount"] or 0
        response.context_data["total_amount"] = total
        return response
