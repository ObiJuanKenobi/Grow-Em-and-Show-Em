from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField(max_length=50, min_length=4)
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']


class RecordTableForm(forms.Form):
    plant = forms.CharField(label="Plant/Variety", max_length='25')
    location = forms.CharField(label="Location", max_length='75')
    quantity = forms.CharField(label="Quantity", max_length='75')
    date = forms.DateField(label="Date")
    notes = forms.CharField(label='Notes', max_length='200')
