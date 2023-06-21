from typing import Any, Mapping, Optional, Type, Union
from django import forms
from django.forms.utils import ErrorList
from django.contrib.auth.models import User
from .models import Profile
from .models import Question
from .models import Answer
from .models import Tag
import os
import re

IMG_DIR = 'static/main/img/'
FIELD_CLASS = 'form-control black_rounded_border'

def set_field(form, field, css_class, p_holder):
    form.fields[field].widget.attrs['class'] = css_class
    form.fields[field].widget.attrs['placeholder'] = p_holder

class LoginForm(forms.Form):
    username = forms.CharField(min_length='4', widget=forms.TextInput)
    password = forms.CharField(min_length='4', widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args,**kwargs)
        set_field(self, 'username', FIELD_CLASS, 'my_login')
        set_field(self, 'password', FIELD_CLASS, 'my_password')

class RegistrationForm(forms.ModelForm):
    password_check = forms.CharField(min_length='4', widget=forms.PasswordInput)
    avatar         = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username','first_name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args,**kwargs)
        self.fields['username'].label = 'Login'
        self.fields['first_name'].label = 'Username'
        set_field(self, 'first_name',     FIELD_CLASS, 'P.B.Parker')
        set_field(self, 'username',       FIELD_CLASS, 'my_login42137')
        set_field(self, 'email',          FIELD_CLASS, 'johndoe@gmail.com')
        set_field(self, 'password',       FIELD_CLASS, 'Password')
        set_field(self, 'password_check', FIELD_CLASS, 'Password')

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Login already exists')
        return username
    
    def clean(self):
        data = self.cleaned_data
        if ('password' in data) & ('password_check' in data): 
            password = self.cleaned_data['password']
            password_check = self.cleaned_data['password_check']
            if password != password_check :
                raise forms.ValidationError('Passwords do not match')
        return self.cleaned_data
    
    def save(self, commit=True):
        user_data = self.cleaned_data
        avatar = user_data.pop('avatar')
        user_data.pop('password_check')
        user = User.objects.create_user(**user_data)
        if avatar:
            Profile.objects.create(user=user, avatar=avatar)
        else:
            Profile.objects.create(user=user)
        return user

class EditForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username','first_name', 'email']

    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args,**kwargs)
        self.fields['username'].label = 'Login'
        self.fields['first_name'].label = 'Username'
        self.fields['username'].error_messages={"invalid": "Enter a valid login. This value may contain only letters, numbers, and @/./+/-/_ characters."}
        set_field(self, 'first_name', FIELD_CLASS, 'P.B.Parker')
        set_field(self, 'username',   FIELD_CLASS, 'my_login42137')
        set_field(self, 'email',      FIELD_CLASS, 'johndoe@gmail.com')

    def clean_username(self):
        new_login = self.cleaned_data['username']
        if 'username' in self.changed_data:
            if User.objects.filter(username=new_login).exists():
                raise forms.ValidationError('Login already exists')
        return new_login
    
    def save(self, commit=True):
        data = self.cleaned_data
        user = super().save(commit)

        if 'avatar' in self.changed_data:
            profile = user.profile
            profile.avatar = data['avatar']
            profile.save()
        return user
    
class AskForm(forms.ModelForm):
    tag = forms.CharField(required=False, max_length=150, widget=forms.TimeInput)
    class Meta:
        model = Question
        fields = ['title', 'text']

    def __init__(self, *args, **kwargs):
        super(AskForm, self).__init__(*args,**kwargs)
        set_field(self, 'title', FIELD_CLASS, 'Title')
        set_field(self, 'text',  FIELD_CLASS, 'Question')
        set_field(self, 'tag',   FIELD_CLASS, 'Some tags')
    
    def save(self, user):
        data = self.cleaned_data
        tag_str = data['tag']
        tags = []
        if tag_str:
            tags = re.split(r'\s+', tag_str)

        data.pop('tag')
        question = Question(**data)
        question.profile = user.profile
        question.save()

        def has(tag, tag_objs):
            for tag_obj in tag_objs:
                if tag==tag_obj.name:
                    return True
            return False
        
        new_tags = []

        tag_objs = Tag.objects.filter(name__in=tags)
        question.tag.set(tag_objs)
        for tag in tags:
            if not has(tag, tag_objs):
                new_tag = Tag(name=tag)
                new_tags.append(new_tag)
        for tag in tag_objs:
            tag.rating += 1
            tag.save()

        Tag.objects.bulk_create(new_tags)
        new_objs = Tag.objects.filter(name__in=new_tags)
        question.tag.add(*new_objs)
        return question

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args,**kwargs)
        set_field(self, 'text', FIELD_CLASS, 'Your answer')
    
    def save(self, user, question):
        data = self.cleaned_data
        answer = Answer(
            text=data['text'],
            profile=user.profile,
            question=question,
        )
        answer.save()
        return answer
    