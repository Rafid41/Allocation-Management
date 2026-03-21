import uuid
from django.db import models

class PBSWise_Summary(models.Model):
    """
    Model for regional history summary reporting. 
    IDs are synchronized with UUID4 standards.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    report_name = models.CharField(max_length=256, default="Regional Inventory Summary")

    def __str__(self):
        return f"{self.report_name} - {self.created_at.strftime('%Y-%m-%d')}"
