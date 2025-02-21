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

    UNIT_CHOICES = [
        ("Nos.", "Nos."),
        ("Mtr.", "Mtr."),
        ("Km.", "Km."),
        ("Set.", "Set."),
        ("Pair.", "Pair."),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    warehouse = models.CharField(
        max_length=50, choices=WAREHOUSE_CHOICES, default="Dhaka"
    )
    unit_of_item = models.CharField(
        max_length=10, choices=UNIT_CHOICES, default="Nos."
    )  # Updated field
    unit_price = models.BigIntegerField(default=0)
    quantity_of_item = models.BigIntegerField(default=0)
    package = models.ForeignKey(
        Package,
        on_delete=models.SET_NULL,
        related_name="package_of_item",
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
