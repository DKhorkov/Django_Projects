from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class BlogPost(models.Model):
    """Модель для создания записей блога."""
    title = models.CharField(max_length=50, help_text='Введите название блога')
    text = models.TextField(help_text='Введите содержимое блога')
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Возврат строки с текстом объекта, а не ссылки на него."""
        return self.title
