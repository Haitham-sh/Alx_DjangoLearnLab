from django import forms
from django.contrib.auth.models import User
from .models import Profile, Comment, Post

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            })
        }

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ['tag']
        widgets = {
            'tag': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a tag',
                'rows': 3,
            })
        }