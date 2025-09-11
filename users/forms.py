from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    is_govt = forms.BooleanField(label="Government User", required=False)
    govt_code = forms.CharField(required=False, label="Government Code")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'is_govt', 'govt_code', 'division', 'district', 'upazila']

    def clean(self):
        cleaned_data = super().clean()
        is_govt = cleaned_data.get('is_govt')
        govt_code = cleaned_data.get('govt_code')

        if is_govt and govt_code != 'THEVOICEBRIDGE':
            raise forms.ValidationError("Invalid Government Code. You are not authorized.")

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['bio', 'profile_pic', 'division', 'district', 'upazila']