# fridge/forms.py
from django import forms
from .models import FoodItem

class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name', 'category', 'quantity', 'best_by', 'storage_location', 'opened']
        widgets = {
            'best_by': forms.DateInput(attrs={'type': 'date'}),
        }

