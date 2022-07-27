from django import forms

from .models import Topic, Entry


class TopicForm(forms.ModelForm):
    """Создает форму для добавления новой темы."""
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}  # Оставляем пустым, поскольку в модели Topic у нас уже прописан вспомогательный текст.


class EntryForm(forms.ModelForm):
    """Создает форму для добавления новой записи к теме."""
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}

        # Устанавливаем зону для ввода текста в размере 80 столбцов вместо 40 по умолчанию:
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}
