from django import forms
from .models import PropertyOwner, InteractionLog


class PropertyOwnerForm(forms.ModelForm):
    class Meta:
        model = PropertyOwner
        fields = [
            'name', 'email', 'phone', 'company_name', 'address',
            'city', 'state', 'zip_code', 'reliability_rating',
            'communication_rating', 'maintenance_rating', 'overall_rating',
            'notes', 'last_contacted', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(123) 456-7890'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'reliability_rating': forms.Select(attrs={'class': 'form-control'}),
            'communication_rating': forms.Select(attrs={'class': 'form-control'}),
            'maintenance_rating': forms.Select(attrs={'class': 'form-control'}),
            'overall_rating': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'last_contacted': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class InteractionLogForm(forms.ModelForm):
    class Meta:
        model = InteractionLog
        fields = ['interaction_type', 'subject', 'notes']
        widgets = {
            'interaction_type': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
