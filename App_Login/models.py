from django.db import models
from django.contrib.auth.models import AbstractUser, User


class User_Group(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_group') 
    STATUS_CHOICES = [
        ("View History and Status only", "View History and Status only"),
        ("Editor", "Editor"), 
        ("Only_View_History_and_Edit_CS&M_Column", "OnlyView History and Edit CS&M Column"),
        ("Only_View_History_and_Edit_Carry_From_Warehouse_Column", "Only View History and Edit Carry_From_Warehouse Column"),
    ]
    user_group_type = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default="View History and Status only"
    )


    def __str__(self):
        return str(self.user.username)