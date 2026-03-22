import uuid
from django.db import models
from App_Entry.models import Item as MainItem

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
    unit = models.CharField(max_length=100, choices=MainItem.UNIT_CHOICES, default="Nos.")
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.item_name

class Zonals_Balance(models.Model):
    """Model to store Zonal Balance records."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pbs = models.ForeignKey(PBS_List, on_delete=models.CASCADE, related_name="zonal_balances")
    zonal = models.ForeignKey(PBS_Zonals, on_delete=models.CASCADE, related_name="zonal_balances")
    item = models.ForeignKey(Zonal_Items, on_delete=models.CASCADE, related_name="zonal_balances")
    
    # Storage Fields (Using Float as per requirements)
    deposit_work = models.FloatField(default=0.0)
    mcep_dmd = models.FloatField(default=0.0)
    mcep_kd = models.FloatField(default=0.0)
    mcep_bd = models.FloatField(default=0.0)
    other = models.FloatField(default=0.0)
    om_store = models.FloatField(default=0.0)
    own_stock = models.FloatField(default=0.0)
    
    total = models.FloatField(default=0.0, editable=False)

    class Meta:
        unique_together = ('pbs', 'zonal', 'item')
        verbose_name_plural = "Zonal Balances"

    def save(self, *args, **kwargs):
        # Calculate sum of all storage fields
        self.total = (
            (self.deposit_work or 0.0) +
            (self.mcep_dmd or 0.0) +
            (self.mcep_kd or 0.0) +
            (self.mcep_bd or 0.0) +
            (self.other or 0.0) +
            (self.om_store or 0.0) +
            (self.own_stock or 0.0)
        )
        super(Zonals_Balance, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.pbs.pbs_name} - {self.zonal.zonal_name} - {self.item.item_name}"
