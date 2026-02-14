from django.db import models

# Create your models here.
import uuid

class PaginationManager(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    table_pagination_limit = models.PositiveIntegerField(default=50)

    def save(self, *args, **kwargs):
        if not self.pk and PaginationManager.objects.exists():
            # If you're trying to save a new instance, but one already exists,
            # update the existing one instead.
            return PaginationManager.objects.first().save(*args, **kwargs)
        return super(PaginationManager, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj = cls.objects.first()
        if not obj:
            obj = cls.objects.create()
        return obj

    def __str__(self):
        return "Pagination Manager"
