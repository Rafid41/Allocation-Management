from django.contrib import admin
from .models import PBS,Temporary_Allocation, Final_Allocation

# Register your models here.
admin.site.register(PBS)
admin.site.register(Temporary_Allocation)
admin.site.register(Final_Allocation)
