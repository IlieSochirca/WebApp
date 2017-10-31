from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields =['first_name', 'last_name', 'email']

class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  # these 2 lines mean that I want to add these 2 fields more to this form
    password2 = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']  # these fields are those we want to take from User Model

    def save(self, commit=True):
        user = super(RegisterUserForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user
    # validation password. this help us check the passwords
    def clean_password2(self):
        cd = self.cleaned_data

        if cd['password']!=cd['password2']:
            raise ValidationError ("Passwords don't match!")
        else:
            return cd['password2']

class UpdateForm(forms.ModelForm):
    image=forms.ImageField()
    phone = forms.IntegerField()
    birth_date = forms.DateField()  # the below fields are added as desired
    hobby = forms.CharField()
    city = forms.CharField()
    current_project = forms.CharField()

    #form fields for updating user
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'birth_date', 'hobby', 'city','current_project', 'image']

