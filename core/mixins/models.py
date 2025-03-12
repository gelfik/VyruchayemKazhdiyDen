from django.db import models
from django.utils import timezone


class DeletedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted__isnull=True)


class CreatedUpdatedMixin(models.Model):
    created = models.DateTimeField("Дата добавления", default=timezone.now)
    updated = models.DateTimeField("Дата изменения", auto_now=True)
    deleted = models.DateTimeField("Дата удаления", null=True, blank=True, db_index=True)

    objects = DeletedManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self._meta.verbose_name} ({self.id})"
