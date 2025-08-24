from django import forms
from Project_App_Allocation.models import Final_Allocation

class FinalAllocationForm(forms.ModelForm):
    class Meta:
        model = Final_Allocation
        fields = ['allocation_no', 'quantity']
