import uuid
from django.db import models

class PBS_List(models.Model):
    """Model to store the list of PBS names."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pbs_name = models.CharField(max_length=256)

    def __str__(self):
        return self.pbs_name
