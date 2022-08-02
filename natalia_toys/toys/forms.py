from django import forms

from .models import Toy


class ToyForm(forms.ModelForm):
    """Форма для создания экземпляра игрушки."""
    class Meta:
        model = Toy
        fields = ['title', 'price', 'image', 'description']
        labels = {'title': "", 'price': "", 'image': "", 'description': ""}
        widgets = {'description': forms.Textarea(attrs={'cols': 100})}
