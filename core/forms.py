from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from core.models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'product_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class':'form-control'}),
        }

class CheckoutAddressForm(forms.Form):

    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '1234 Main St'
    }))
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Apartment or suite'
    }))
    country = CountryField(blank_label='Select Country').formfield(widget=CountrySelectWidget(attrs={
        'class': 'form-control',
    }))
    zip_code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))