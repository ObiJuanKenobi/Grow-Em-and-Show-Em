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
    year = forms.CharField(label='Year', min_length='4', widget=forms.TextInput(attrs={'placeholder': 'Ex. 2017'}))
    month = forms.CharField(label='Month', min_length='2', widget=forms.TextInput(attrs={'placeholder': 'Ex. 29'}))
    date = forms.CharField(label='Day', min_length='2', widget=forms.TextInput(attrs={'placeholder': 'Ex. 04'}))
    notes = forms.CharField(label='Notes', max_length='200', widget=forms.Textarea(attrs={'placeholder': 'Warning! This will be publically displayed'}))
