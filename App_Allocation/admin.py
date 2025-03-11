from django.contrib import admin
from .models import PBS,Temporary_Allocation, Final_Allocation, Allocation_Number

# Register your models here.
admin.site.register(Allocation_Number)
admin.site.register(PBS)
admin.site.register(Temporary_Allocation)
admin.site.register(Final_Allocation)
