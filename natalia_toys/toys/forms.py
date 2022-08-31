from django import forms

from .models import Toy


class ToyForm(forms.ModelForm):
    """Форма для создания экземпляра игрушки."""
    class Meta:
        model = Toy
        fields = ['title', 'price', 'image_1', 'image_2', 'image_3', 'image_4', 'description', 'is_available']
        labels = {'image_1': "Изображение 1", 'image_2': "Изображение 2", 'image_3': "Изображение 3",
                  'image_4': "Изображение 4", 'is_available': "Имеется в наличии?"}
        widgets = {'description': forms.Textarea(attrs={'cols': 100})}
