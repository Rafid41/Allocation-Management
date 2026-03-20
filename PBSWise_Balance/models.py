import uuid
from django.db import models

class PBS_List(models.Model):
    """Model to store the list of PBS names."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pbs_name = models.CharField(max_length=256)

    def __str__(self):
        return self.pbs_name

class PBS_Zonals(models.Model):
    """Model to store Zonal units (HQ, Zonal, Sub-Zonal) for each PBS."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pbs = models.ForeignKey(PBS_List, on_delete=models.CASCADE, related_name='zonals')
    zonal_name = models.CharField(max_length=256)
    
    ZONAL_CHOICES = [
        ('HQ', 'HQ'),
        ('Zonal', 'Zonal'),
        ('Sub-Zonal', 'Sub-Zonal'),
    ]
    zonal_type = models.CharField(max_length=50, choices=ZONAL_CHOICES)

    def __str__(self):
        return f"{self.pbs.pbs_name} - {self.zonal_name} ({self.zonal_type})"

class Zonal_Items(models.Model):
    """Model to store Items for zonal balance management."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item_name = models.CharField(max_length=256)

    def __str__(self):
        return self.item_name
