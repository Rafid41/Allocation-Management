import uuid
from django.db import models

class StoreWise_Summary(models.Model):
    """
    Model for regional storewise summary reporting. 
    IDs are synchronized with UUID4 standards for high-security auditing.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    store_category = models.CharField(max_length=256, default="Regional Store Category")

    def __str__(self):
        return f"{self.store_category} - {self.created_at.strftime('%Y-%m-%d')}"

class Meta:
    verbose_name_plural = "Storewise Summaries"
