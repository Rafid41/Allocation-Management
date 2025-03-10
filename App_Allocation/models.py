from django.db import models
from App_Entry.models import Package, Item

# Create your models here.
class PBS(models.Model):
    name = models.TextField(unique=True)

    def __str__(self):
        return self.name
    


class Temporary_Allocation(models.Model):
    allocation_no = models.IntegerField(unique=True)  # Unique allocation number
    item_primary_key = models.IntegerField(null=True)  # Placeholder: primary key of the selected item
    pbs = models.ForeignKey(PBS, on_delete=models.CASCADE)  # Dropdown from PBS model
    package = models.ForeignKey(Package, on_delete=models.CASCADE)  # Locked until PBS is selected
    item = models.ForeignKey(Item, on_delete=models.CASCADE)  # Locked until Package is selected
    warehouse = models.CharField(max_length=50)  # Locked until Item is selected
    quantity = models.IntegerField()  # Placeholder: max available quantity from Item model
    price = models.BigIntegerField()  # Auto-fetched from Item model (not editable)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Allocation {self.allocation_no}"
    

class Final_Allocation(models.Model):
    allocation_no = models.IntegerField(unique=True)  # Unique allocation number
    item_primary_key = models.IntegerField(null=True) 
    pbs = models.ForeignKey(PBS, on_delete=models.CASCADE)  # Dropdown from PBS model
    package = models.ForeignKey(Package, on_delete=models.CASCADE)  # Locked until PBS is selected
    item = models.ForeignKey(Item, on_delete=models.CASCADE)  # Locked until Package is selected
    warehouse = models.CharField(max_length=50)  # Locked until Item is selected
    quantity = models.IntegerField()  # Placeholder: max available quantity from Item model
    price = models.BigIntegerField()  # Auto-fetched from Item model (not editable)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Allocation {self.allocation_no}"