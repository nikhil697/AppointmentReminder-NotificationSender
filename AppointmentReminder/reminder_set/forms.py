from django import forms
from .models import collectdata

class CollectDataForm(forms.ModelForm):
    date = forms.DateField(input_formats=['%Y-%m-%d'])
    time = forms.TimeField(input_formats=['%H:%M:%S'])
    
    class Meta:
        model = collectdata
        fields = ['title', 'date', 'time', 'description']