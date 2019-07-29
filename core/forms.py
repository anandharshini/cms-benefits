from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import EmployeeDependent, HeightWeight
from django.contrib.admin import widgets 
from django.forms import modelformset_factory

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')

    class Meta:
        model = User
        fields = ('username', 'email', 'birth_date', 'password1', 'password2', )

class HeightWeightForm(forms.ModelForm):
    class Meta:
        model = HeightWeight
        exclude=()

DependentsFormset = modelformset_factory(
    EmployeeDependent,
    fields='__all__',
    extra=1
)