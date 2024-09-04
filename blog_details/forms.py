# from typing import Any
from django import forms
from .models import BlogPost, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username or Email'
        })

        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })

class SearchForm(forms.Form):
    query = forms.CharField()

class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ("username", "email")
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
        }
        
    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email has been registered already')
        return data
    
    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            raise forms.ValidationError('username not available')
        return data




class CreatePostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = "__all__"
        exclude = ("slug","date")
        labels = {
            "title" : "Blog Post Title",
            "subtitle" : "Subtitle",
            "author" :  "Your Name",
            "content" : "Body",
            "img_url" : "Blog Image URL",
            "tag" : "Tag",
        }
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'subtitle': forms.TextInput(attrs={'class':'form-control'}),
            'author': forms.Select(attrs={'class':'form-control'}),
            'img_url': forms.FileInput(attrs={'class':'form-control'}),
            'tag': forms.SelectMultiple(attrs={'class':'form-control'}),
            'content': forms.Textarea(attrs={'class':'form-control', "rows": 2}),
        }

class ContactForm(forms.Form):
     name = forms.CharField(max_length=100, label="Name", widget=forms.TextInput(attrs={
        'class': "form-control",
        'placeholder': 'Name'
         }))
     email = forms.EmailField(label="Email Address", widget=forms.TextInput(attrs={
        'class': "form-control",
        'placeholder': 'Email Address'
         }))
     phone = forms.CharField(label="Phone number", widget=forms.TextInput(attrs={
        'class': "form-control",
        'placeholder': 'Phone Number'
         }))
     message = forms.CharField(widget=forms.Textarea(attrs={
        'class': "form-control",
        'placeholder': 'Message', 
        'rows': 5,
         }))

class CommentPostForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("comment_details",)
        labels = {'comment_details': "Write a comment here"}
        widgets = {'comment_details': forms.Textarea(attrs={'class':'form-control', 'rows': 2}),}






