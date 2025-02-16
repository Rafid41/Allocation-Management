from django.db import models


class Package(models.Model):
    packageId = models.BigIntegerField(unique=True)

    def __str__(self):
        return str(self.packageId)  # Convert packageId to a string


class Item(models.Model):
    WAREHOUSE_CHOICES = [
        ("Dhaka", "Dhaka"),
        ("Khulna", "Khulna"),
        ("Chittagong", "Chittagong"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    warehouse = models.CharField(
        max_length=50, choices=WAREHOUSE_CHOICES, default="Dhaka"
    )
    unit_of_item = models.IntegerField(default=0)
    unit_price = models.BigIntegerField(default=0)
    quantity_of_item = models.BigIntegerField(default=0)
    package = models.ForeignKey(
        Package,
        on_delete=models.SET_NULL,  # This will set the package field to null when the item is deleted
        related_name="package_of_item",
        null=True,  # Allow null values in the package field
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Auto capture entry datess

    def __str__(self):
        return self.name
