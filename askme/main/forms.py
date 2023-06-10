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
    login          = forms.CharField(min_length='4', widget=forms.TextInput)
    password       = forms.CharField(min_length='4', widget=forms.PasswordInput)
    password_check = forms.CharField(min_length='4', widget=forms.PasswordInput)
    avatar         = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args,**kwargs)
        set_field(self, 'username',       FIELD_CLASS, 'P.B.Parker')
        set_field(self, 'login',          FIELD_CLASS, 'my_login42137')
        set_field(self, 'email',          FIELD_CLASS, 'johndoe@gmail.com')
        set_field(self, 'password',       FIELD_CLASS, 'Password')
        set_field(self, 'password_check', FIELD_CLASS, 'Password')
    
    def clean(self):
        if not self._errors:
            password = self.cleaned_data['password']
            password_check = self.cleaned_data['password_check']
            if password != password_check :
                raise forms.ValidationError('Passwords do not match')
            if User.objects.filter(username=self.cleaned_data['login']).exists():
                raise forms.ValidationError('Login already exists')
        return self.cleaned_data
    
    def save(self):
        data = self.cleaned_data
        user = User.objects.create_user(username=data['login'],
                                        first_name=data['username'],
                                        email=data['email'],
                                        password=data['password'])
        Profile.objects.create(profile=user, avatar=data['avatar'], rating=0)
        return user

class EditForm(forms.ModelForm):
    login  = forms.CharField(min_length='4', widget=forms.TextInput)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args,**kwargs)
        set_field(self, 'username', FIELD_CLASS, 'P.B.Parker')
        set_field(self, 'login',    FIELD_CLASS, 'my_login42137')
        set_field(self, 'email',    FIELD_CLASS, 'johndoe@gmail.com')

    def clean(self):
        if not self._errors:
            if User.objects.filter(username=self.cleaned_data['login']).exists():
                raise forms.ValidationError('Login already exists')
        return self.cleaned_data
    
    def save(self, user):
        data = self.cleaned_data
        user.username = data['login']
        user.first_name = data['username']
        user.email = data['email']
        if data['avatar']:
            path_to_avatar = os.path.join(IMG_DIR, str(user.id) + '.png')
            if os.path.isfile(path_to_avatar):
                os.remove(path_to_avatar)
            user.profile.avatar = data['avatar']
            user.profile.save()

        user.save()
        return user
    
class AskForm(forms.ModelForm):
    tag = forms.CharField(min_length=4, max_length=150, widget=forms.TimeInput)
    class Meta:
        model = Question
        fields = ['title', 'text']

    def __init__(self, *args, **kwargs):
        super(AskForm, self).__init__(*args,**kwargs)
        set_field(self, 'title', FIELD_CLASS, 'Title')
        set_field(self, 'text',  FIELD_CLASS, 'Question')
        set_field(self, 'tag',   FIELD_CLASS, 'Some tags')

    # def clean(self):
    #     return self.cleaned_data
    
    def save(self, user):
        data = self.cleaned_data
        tags = re.split(r'\s+', data['tag'])
        data.pop('tag')
        data['rating'] = 0
        question = Question(**data)
        question.user_id = user.profile
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
                new_tag = Tag(name=tag, rating=1)
                new_tags.append(new_tag)
        for tag in tag_objs:
            tag.rating += 1
            tag.save()

        print(new_tags)
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

    def clean(self):
        # raise forms.ValidationError('Just Error')
        return self.cleaned_data
    
    def save(self, user, question):
        data = self.cleaned_data
        answer = Answer(
            text=data['text'],
            user_id=user.profile,
            question_id=question,
            rating=0,
            correct=False,
        )
        answer.save()
        return answer