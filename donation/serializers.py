from rest_framework import serializers

from donation.models import PromoDonation


class NewPromoDonationPaymentSerializer(serializers.Serializer):
    orderid = serializers.IntegerField(required=True)
    amount = serializers.IntegerField(required=True)


class NewPromoDonationWebhookSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, allow_blank=False)
    email = serializers.EmailField(required=True, allow_blank=False)
    payment = NewPromoDonationPaymentSerializer(required=True)

    @property
    def cleaned_data(self):
        data = self.validated_data
        payment_data = data.pop("payment")
        data["order_id"] = payment_data["orderid"]
        data["amount"] = payment_data["amount"]
        return data


class PublicPromoDonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoDonation
        fields = ("created", "amount")
