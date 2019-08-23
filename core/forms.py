from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import EmployeeDependent, HeightWeight, LookupModel
from django.contrib.admin import widgets 
from django.forms import modelformset_factory
from employer.models import Employer
class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.', required=True)
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD', required=True)
    employer = forms.ModelChoiceField(queryset=Employer.objects.all(), required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'birth_date', 'employer', 'password1', 'password2', )

class HeightWeightForm(forms.ModelForm):
    class Meta:
        model = HeightWeight
        exclude=()

DependentsFormset = modelformset_factory(
    EmployeeDependent,
    fields='__all__',
    extra=1
)

class EmployeeDependentForm(forms.ModelForm):
    class Meta:
        model = EmployeeDependent
        exclude=('employee','age',)
        widgets = {
             'ssn': forms.TextInput(attrs={'class': 'masked', 'pattern': '^([1-9])(?!\1{2}-\1{2}-\1{4})[1-9]{2}-[1-9]{2}-[1-9]{4}$', 'placeholder': '999-99-9999'}),
             'dob_dependent': forms.DateInput(format='%d/%m/%Y', attrs={'class': 'masked', 'pattern': '^(((0?[1-9]|1[012])/(0?[1-9]|1\d|2[0-8])|(0?[13456789]|1[012])/(29|30)|(0?[13578]|1[02])/31)/(19|[2-9]\d)\d{2}|0?2/29/((19|[2-9]\d)(0[48]|[2468][048]|[13579][26])|(([2468][048]|[3579][26])00)))$', 'placeholder': 'MM/dd/yyyy'})
        }
        # 'tobacco_use': forms.CheckboxInput(attrs={ 'style': 'width:50px; height: 50px;' }),
    
    def __init__(self, *args, **kwargs):
        super(EmployeeDependentForm, self).__init__(*args, **kwargs)
        self.fields['tobacco_use'].queryset = LookupModel.objects.filter(type_lookup='yes_no')
        self.fields['relationship'].queryset = LookupModel.objects.filter(type_lookup='employee_relationship')
        self.fields['gender'].queryset = LookupModel.objects.filter(type_lookup='gender')
        self.header = 'Dependents'

class SignatureForm(forms.Form):
    sign_data = forms.CharField(max_length=1024)