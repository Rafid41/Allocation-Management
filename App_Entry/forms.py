# forms.py
from django import forms
from .models import Package


# class PackageForm(forms.ModelForm):
#     class Meta:
#         model = Package
#         fields = ["name", "description", "warehouse", "unit"]


# class PackageItemForm(forms.ModelForm):
#     class Meta:
#         model = PackageItem
#         fields = ["package", "item", "quantity_of_item", "unit_price_of_item"]
