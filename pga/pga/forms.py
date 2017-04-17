from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']


class RecordTableForm(forms.Form):
    plant = forms.CharField(label="Plant/Variety", max_length='100')
    location = forms.CharField(label="Location", max_length='100')
    quantity = forms.CharField(label="Quantity", max_length='100')
    date = forms.CharField(label="Date", max_length='100')
    notes = forms.CharField(label="Notes")
