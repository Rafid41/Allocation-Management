from django.db import models
from django.contrib.auth.models import AbstractUser, User


class User_Group(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ("View History and Status only", "View History and Status only"),
        ("Editor", "Editor"), 
        ("Only View History and Edit CS&M Column", "Only View History and Edit CS&M Column"),
        ("Only View History and Edit Carry_From_Warehouse Column", "Only View History and Edit Carry_From_Warehouse Column"),
    ]
    user_group_type = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default="View History and Status only"
    )


    def __str__(self):
        return str(self.user.username)