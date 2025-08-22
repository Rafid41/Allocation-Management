from django.contrib import admin
from .models import Temporary_Allocation, Final_Allocation, Allocation_Number, PBS
# Register your models here.
admin.site.register(Temporary_Allocation)
admin.site.register(Final_Allocation)
admin.site.register(Allocation_Number)
admin.site.register(PBS)
