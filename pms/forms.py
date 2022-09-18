from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from pms.models import Drug, Order


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2',)


class DrugForm(forms.ModelForm):
    class Meta:
        model = Drug
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'})
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'date': forms.HiddenInput(),
            'buyer': forms.HiddenInput(),
        }
