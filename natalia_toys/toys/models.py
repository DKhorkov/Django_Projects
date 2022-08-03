from django.db import models
from PIL import Image

# Create your models here.


class Toy(models.Model):
    """Класс для представления модели одной игрушки."""
    title = models.CharField(max_length=50, help_text='Название игрушки')
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Цена игрушки')
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/')
    description = models.TextField(blank=True, help_text='Описание игрушки')

    def __str__(self):
        return self.title

    # Стандартизирует каждое загруженное изображение в превью:
    def save(self):
        super().save()
        img = Image.open(self.image.path)

        if img.height > 100 or img.width > 100:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
