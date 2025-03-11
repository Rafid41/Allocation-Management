from django.db import models
from App_Entry.models import Package, Item

class PBS(models.Model):
    name = models.TextField(unique=True)

    def __str__(self):
        return self.name

class Allocation_Number(models.Model):
    allocation_no = models.IntegerField(unique=True)  # Unique allocation number

    def __str__(self):
        return self.allocation_no

class Temporary_Allocation(models.Model):
    allocation_no = models.ForeignKey(Allocation_Number, on_delete=models.CASCADE)  # Deletes related allocations when removed
    item_primary_key = models.IntegerField(null=True)  
    pbs = models.ForeignKey(PBS, on_delete=models.CASCADE)  
    package = models.ForeignKey(Package, on_delete=models.CASCADE)  
    item = models.ForeignKey(Item, on_delete=models.CASCADE)  
    warehouse = models.CharField(max_length=50)  
    quantity = models.IntegerField()  
    price = models.BigIntegerField()  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Temporary Allocation {self.allocation_no}"

class Final_Allocation(models.Model):
    allocation_no = models.ForeignKey(Allocation_Number, on_delete=models.CASCADE)  # Deletes related allocations when removed
    item_primary_key = models.IntegerField(null=True)  
    pbs = models.ForeignKey(PBS, on_delete=models.CASCADE)  
    package = models.ForeignKey(Package, on_delete=models.CASCADE)  
    item = models.ForeignKey(Item, on_delete=models.CASCADE)  
    warehouse = models.CharField(max_length=50)  
    quantity = models.IntegerField()  
    price = models.BigIntegerField()  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Final Allocation {self.allocation_no}"
