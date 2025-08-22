from django.db import models
from Project_App_Entry.models import Project, Project_Item
from django.contrib.auth.models import User

class PBS(models.Model):
    name = models.TextField(unique=True)

    def __str__(self):
        return str(self.name)

class Allocation_Number(models.Model):
    allocation_no = models.IntegerField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="project_allocation_numbers")
    STATUS_CHOICES = [
        ("Pending Approval", "Pending Approval"),
        ("Allocated", "Allocated"),
        ("Cancelled", "Cancelled"),
        ("Modified", "Modified"),
    ]
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default="Pending Approval"
    )


    def __str__(self):
        return str(self.allocation_no)

class Temporary_Allocation(models.Model):
    allocation_no = models.ForeignKey(Allocation_Number, on_delete=models.CASCADE)  # Deletes related allocations when removed
    item_primary_key = models.IntegerField(null=True)  
    pbs = models.ForeignKey(PBS, on_delete=models.CASCADE)  
    project = models.ForeignKey(Project, on_delete=models.CASCADE)  
    item = models.ForeignKey(Project_Item, on_delete=models.CASCADE)
    unit_of_item = models.TextField()  
    warehouse = models.CharField(max_length=50)  
    quantity = models.IntegerField()  
    # price = models.DecimalField(max_digits=15, decimal_places=2)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.allocation_no)

class Final_Allocation(models.Model):
    allocation_no = models.ForeignKey(Allocation_Number, on_delete=models.CASCADE)  # Deletes related allocations when removed
    item_primary_key = models.IntegerField(null=True)  
    pbs = models.ForeignKey(PBS, on_delete=models.CASCADE)  
    project = models.ForeignKey(Project, on_delete=models.CASCADE)  
    item = models.ForeignKey(Project_Item, on_delete=models.CASCADE)  
    unit_of_item = models.TextField()
    warehouse = models.CharField(max_length=50)  
    quantity = models.IntegerField()  
    # price = models.DecimalField(max_digits=15, decimal_places=2)  
    created_at = models.DateTimeField(auto_now_add=True)




    def __str__(self):
        return str(self.allocation_no)