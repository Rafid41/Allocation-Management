from django import forms
from .models import Temporary_Allocation

class TemporaryAllocationForm(forms.ModelForm):
    class Meta:
        model = Temporary_Allocation
        fields = ['allocation_no', 'quantity']
