from django.db import models
from django.utils.timezone import now
from django.utils import timezone

class Package(models.Model):
    packageId = models.TextField(unique=True)

    def __str__(self):
        return str(self.packageId)  # Convert packageId to a string


class Item(models.Model):
    WAREHOUSE_CHOICES = [
        ("Dhaka", "Dhaka"),
        ("Khulna", "Khulna"),
        ("Chittagong", "Chittagong"),
    ]

    UNIT_CHOICES = [
        ("Nos.", "Nos."),
        ("Mtr.", "Mtr."),
        ("Km.", "Km."),
        ("Set.", "Set."),
        ("Pair.", "Pair."),
        ("Kg", "Kg"),
        ("Lot", "Lot"),
        ("Pcs", "Pcs"),
        ("Coil", "Coil"),
        ("Box", "Box"),
        ("Feet", "Feet"),
        ("Liter", "Liter"),
        ("m3", "m3"),
        ("m2", "m2"),
        ("Ream", "Ream"),
        ("Bundle", "Bundle"),
        ("Carton", "Carton"),
    ]


    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    warehouse = models.CharField(
        max_length=50, choices=WAREHOUSE_CHOICES, default="Dhaka"
    )
    unit_of_item = models.CharField(
        max_length=100, choices=UNIT_CHOICES, default="Nos."
    )  # Updated field
    unit_price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    quantity_of_item = models.DecimalField(
        max_digits=20,    
        decimal_places=3,  
        default=0.00
    )

    package = models.ForeignKey(
        Package,
        on_delete=models.SET_NULL,
        related_name="package_of_item",
        null=True,
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.name)
