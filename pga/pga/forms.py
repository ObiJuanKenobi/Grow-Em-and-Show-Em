from django.contrib.auth.models import User
from django import forms

from pga.dataAccess import DataAccess


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField(max_length=50, min_length=4)
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']


class RecordTableFormWithQuantity(forms.Form):
    db = DataAccess()

    crop_choices = db.get_current_crops()
    crop_tuples = []
    crop_subtype_tuples = []
    for crop_choice in crop_choices:
        crop_tuples.append((crop_choice['name'], crop_choice['name']))

        for subtype in crop_choice['subtypes']:
            crop_subtype_tuples.append((crop_choice['name'], subtype))

    crop_choices_tuples = tuple(crop_tuples)
    crop_subtype_tuples_tuple = tuple(crop_subtype_tuples)

    unit_choices = (('Ounces', 'Ounces'), ('Pounds', 'Pounds'), ('Plants', 'Plants'))

    garden_choices = db.get_gardens()
    garden_tuples = []
    for garden_choice in garden_choices:
        garden_tuples.append((garden_choice, garden_choice))
    garden_choices_tuples = tuple(garden_tuples)

    crop = forms.ChoiceField(widget=forms.Select, choices=crop_choices_tuples)
    # subtypes = forms.ChoiceField(widget=forms.Select, choices=crop_subtype_tuples_tuple)
    location = forms.ChoiceField(widget=forms.Select, choices=garden_choices_tuples)

    quantity = forms.FloatField(max_value=1000, min_value=1)

    units = forms.ChoiceField(widget=forms.Select, choices=unit_choices)



class RecordTableFormWithNotes(forms.Form):
    db = DataAccess()

    crop_choices = db.get_current_crops()
    crop_choices.append('Other/Multiple')
    crop_tuples = []
    for crop_choice in crop_choices:
        crop_tuples.append((crop_choice, crop_choice))
    crop_choices_tuples = tuple(crop_tuples)

    garden_choices = db.get_gardens()
    garden_choices.append('Other/Multiple')
    garden_tuples = []
    for garden_choice in garden_choices:
        garden_tuples.append((garden_choice, garden_choice))
    garden_choices_tuples = tuple(garden_tuples)

    crop = forms.ChoiceField(widget=forms.Select, choices=crop_choices_tuples)
    location = forms.ChoiceField(widget=forms.Select, choices=garden_choices_tuples)

    notes = forms.CharField(max_length='512', widget=forms.Textarea(attrs={'placeholder': 'Notes', 'style': 'height: 2em;'}))