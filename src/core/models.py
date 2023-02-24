from django.db import models
from django.utils.translation import gettext_lazy as _


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Дата обновления"), auto_now=True)

    class Meta:
        abstract = True
        get_latest_by = "updated_at"


class ActiveObjectsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class IsActiveModel(models.Model):
    is_active = models.BooleanField("Активный", default=False)

    objects = models.Manager()
    active_objects = ActiveObjectsManager()

    class Meta:
        abstract = True
