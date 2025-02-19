from django import forms
from .models import BlogPost, Comment, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class BlogPostForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select a Category", required=True)

    class Meta:  # ✅ Proper indentation
        model = BlogPost
        fields = ['title', 'content', 'category', 'image', 'published']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
