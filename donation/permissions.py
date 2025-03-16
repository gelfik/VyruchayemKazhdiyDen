from django.conf import settings
from rest_framework import permissions


class WebhookAPIPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        """Проверка API ключа в заголовке"""

        return request.headers.get("X-Api-Key", "") == settings.TILDA_WEBHOOK_API_KEY
