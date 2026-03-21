import uuid
from django.db import models
from PBSWise_Balance.models import PBS_List, PBS_Zonals, Zonal_Items

class PBS_History(models.Model):
    """Model to log all Transfer and Withdrawal operations in the PBSWise Inventory ecosystem."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pbs = models.ForeignKey(PBS_List, on_delete=models.CASCADE, related_name="history_logs")
    item = models.ForeignKey(Zonal_Items, on_delete=models.CASCADE, related_name="history_logs")
    quantity = models.FloatField()
    
    ACTION_CHOICES = [
        ('Transfer Item', 'Transfer Item'),
        ('Withdraw Item', 'Withdraw Item'),
    ]
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    
    # Source Details
    zonal_from = models.ForeignKey(PBS_Zonals, on_delete=models.CASCADE, related_name="history_from")
    store_from = models.CharField(max_length=100)
    
    # Destination Details (Optional for Withdrawal)
    zonal_to = models.ForeignKey(PBS_Zonals, on_delete=models.SET_NULL, null=True, blank=True, related_name="history_to")
    store_to = models.CharField(max_length=100, null=True, blank=True)
    
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "PBS History Logs"
        ordering = ['-date']

    def __str__(self):
        return f"{self.pbs.pbs_name} - {self.action} - {self.item.item_name} ({self.date.strftime('%d-%m-%Y')})"
