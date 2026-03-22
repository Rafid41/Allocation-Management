from django.contrib import admin
from .models import PBS_List, PBS_Zonals, Zonal_Items, Zonals_Balance

# Register your models here.
admin.site.register(PBS_List)
admin.site.register(PBS_Zonals)
admin.site.register(Zonal_Items)
admin.site.register(Zonals_Balance)
