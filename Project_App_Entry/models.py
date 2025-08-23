from django.db import models
from django.utils.timezone import now
from django.utils import timezone

class Project(models.Model):
    projectId = models.TextField(unique=True)

    def __str__(self):
        return str(self.projectId)  # Convert projectId to a string


class Project_Item(models.Model):
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
    quantity_of_item = models.BigIntegerField(default=0)
    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        related_name="project_of_item",
        null=True,
    )
    created_at = models.DateTimeField(default=timezone.now)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.name)
