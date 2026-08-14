from django import forms
from .models import Location, Item


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Kitchen Pantry, Master Bedroom, Garage',
                'autocomplete': 'off',
            })
        }
        labels = {
            'name': 'Location Name',
        }
        help_texts = {
            'name': 'Enter a unique name for this location in your household.',
        }


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'location', 'quantity', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Blender, Power Drill, Spare Lightbulbs',
                'autocomplete': 'off',
            }),
            'location': forms.Select(attrs={
                'class': 'form-control form-select',
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '1',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Optional details such as serial numbers, purchase date, or exact shelf location...',
            }),
        }
        labels = {
            'name': 'Item Name',
            'location': 'Location',
            'quantity': 'Quantity',
            'description': 'Description',
        }
        help_texts = {
            'name': 'The name of the household item.',
            'location': 'Select where this item is stored.',
            'quantity': 'Current quantity on hand.',
            'description': 'Additional notes or specifications (optional).',
        }
