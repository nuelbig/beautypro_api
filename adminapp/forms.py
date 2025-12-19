from django import forms
from .models import rdv

class RdvForm(forms.ModelForm):
    class Meta:
        model = rdv
        fields = ['client', 'telephone', 'service', 'date', 'heure']
        widgets = {
            'client': forms.TextInput(attrs={
                'class': 'border-border w-full p-3 rounded-md',
                'placeholder': 'Votre nom et prénom'
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'border-border w-full p-3 rounded-md',
                'placeholder': '+228 90 00 00 00'
            }),
            'service': forms.TextInput(attrs={
                'class': 'border-border w-full p-3 rounded-md',
                'placeholder': 'Service demandé'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'border-border w-full p-3 rounded-md'
            }),
            'heure': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'border-border w-full p-3 rounded-md'
            }),
        }
