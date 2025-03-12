from django.contrib import admin

from donation.models import PromoDonation


# Register your models here.

@admin.register(PromoDonation)
class PromoDonationAdmin(admin.ModelAdmin):
    change_list_template = "admin/donation/change_list_promo_donation.html"
    list_display = (
        "id",
        "email",
        "amount",
        "created",
    )

    def has_change_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["total_amount"] = (
            self.get_queryset(request).aggregate(total_amount=Sum("amount")).get("total_amount", 0)
        )
        return super().changelist_view(request, extra_context=extra_context)
