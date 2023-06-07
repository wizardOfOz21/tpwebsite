from typing import Any, Mapping, Optional, Type, Union
from django import forms
from django.forms.utils import ErrorList
from django.contrib.auth.models import User
from .views import Profile

FIELD_CLASS = 'form-control black_rounded_border'

def set_field(form, field, css_class, p_holder, max_length):
    form.fields[field].widget.attrs['class'] = css_class
    form.fields[field].widget.attrs['placeholder'] = p_holder
    form.fields[field].widget.attrs['maxlength'] = max_length


class LoginForm(forms.Form):
    username = forms.CharField(min_length='4', widget=forms.TextInput)
    password = forms.CharField(min_length='4', widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args,**kwargs)
        set_field(self, 'username', FIELD_CLASS, 'my_login', '50')
        set_field(self, 'password', FIELD_CLASS, 'my_password', '100')

class RegistrationForm(forms.ModelForm):
    login          = forms.CharField(min_length='4', widget=forms.TextInput)
    password       = forms.CharField(min_length='4', widget=forms.PasswordInput)
    password_check = forms.CharField(min_length='4', widget=forms.PasswordInput)
    avatar         = forms.ImageField()

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args,**kwargs)
        set_field(self, 'username', FIELD_CLASS, 'P.B.Parker', '50')
        set_field(self, 'login', FIELD_CLASS, 'my_login42137', '50')
        set_field(self, 'email', FIELD_CLASS, 'johndoe@gmail.com', '100')
        set_field(self, 'password', FIELD_CLASS, 'Password', '100')
        set_field(self, 'password_check', FIELD_CLASS, 'Password', '100')

    def clean(self):
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']
        if password != password_check :
            raise forms.ValidationError('Passwords do not match')
        return self.cleaned_data
    
    def save(self):
        data = self.cleaned_data
        user = User.objects.create_user(username=data['login'],
                                 first_name=data['username'],
                                 email=data['email'],
                                 password=data['password'])
        Profile.objects.create(profile=user, avatar=data['avatar'], rating=0)
        return user
