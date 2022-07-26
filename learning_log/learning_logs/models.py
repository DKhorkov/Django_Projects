from django.db import models

# Create your models here.


class Topic(models.Model):
    """Тема, которую изучает пользователь."""
    text = models.CharField(max_length=200, help_text='Введите название темы.')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Возвращает строковое представление модели.
        При вводе информации о теме возвращает атрибут по умолчанию - текст."""
        return self.text


class Entry(models.Model):
    """Информация, изученная пользователем по теме."""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)  # При удалении темы все записи тоже удаляются.
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        """В случае обращения к 2 и более записям будет использовано корректное множественное число слово Entry."""
        verbose_name_plural = 'entries'

    def __str__(self):
        """Возвращает строковое представление модели (текст, а не ссылку на объект) в размере первых 50 символов."""
        if len(str(self.text)) < 51:
            return self.text
        else:
            return f'{self.text[:50]}...'
