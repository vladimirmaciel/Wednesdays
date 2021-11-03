from django import forms
from django.forms import ModelForm, fields
from .models import Venue


# Criar a venue form 
class VenueForm(ModelForm):
    class Meta:
        model = Venue
        # fields = "__all__" # mostra todos os campos do model 
        fields = ('name','address','zip_code','phone','web','email_address')
        
        #deixamos as labels vazias apenas com o placeholder
        labels = {
			'name': '',
			'address': '',
			'zip_code': '',
			'phone': '',
			'web': '',
			'email_address': '',			
		}
            
        
        # deixar no padrão bootstrap
        widgets = {
                'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Venue Name'}),
                'address': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address'}),
                'zip_code': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zip Code'}),
                'phone': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone'}),
                'web': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Web Address'}),
                'email_address': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}),
            }
        
        