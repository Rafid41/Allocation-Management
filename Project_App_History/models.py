from django.db import models

# Create your models here.
class Project_History(models.Model):
    allocation_no = models.IntegerField() 
    pbs = models.TextField()  
    project = models.TextField()
    item = models.TextField() 
    warehouse = models.CharField(max_length=50)  
    unit_of_item = models.TextField()  
    quantity = models.DecimalField(
        max_digits=20,    
        decimal_places=3,  
        default=0.00
    )   
    created_at = models.DateTimeField(auto_now=True) 
    STATUS_CHOICES = [
        ("Pending Approval", "Pending Approval"),
        ("Allocated", "Allocated"),
        ("Cancelled", "Cancelled"),
        ("Modified", "Modified"),
    ]
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default="Allocated"
    )
    remarks = models.TextField(blank=True, null=True)
    # CS_and_M = models.DateTimeField(blank=True, null=True)
    carry_from_warehouse = models.DateTimeField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.allocation_no)