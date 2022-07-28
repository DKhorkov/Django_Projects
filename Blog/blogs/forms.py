from django import forms

from .models import BlogPost


class NewBlogForm(forms.ModelForm):
    """Форма для создания нового блога."""
    class Meta:
        model = BlogPost
        fields = ['title', 'text']
        labels = {'title': '', 'text': ''}
