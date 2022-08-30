from django.db import models
from PIL import Image

# Create your models here.


class Toy(models.Model):
    """Модель игрушки."""
    title = models.CharField(max_length=50, help_text='Название игрушки', verbose_name="Название")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Цена игрушки', verbose_name="Цена")
    date_added = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, help_text='Описание игрушки', verbose_name="Описание")
    image_1 = models.ImageField(upload_to='images/', blank=True, help_text='Изображений 1')
    image_2 = models.ImageField(upload_to='images/', blank=True, help_text='Изображений 2')
    image_3 = models.ImageField(upload_to='images/', blank=True, help_text='Изображений 3')
    image_4 = models.ImageField(upload_to='images/', blank=True, help_text='Изображений 4')
    is_available = models.BooleanField(help_text='Имеется в наличии?')

    def __str__(self):
        return self.title

    # Стандартизирует каждое загруженное изображение в превью:
    def save(self):
        """Метод сохранения изображений в БД. Если изображение было добавлено при создании игрушки, оно будет
        от масштабировано согласно указанному в атрибуте "output_size" размеру."""
        super().save()
        output_size = (300, 300)

        if self.image_1:
            img_1 = Image.open(self.image_1.path)
            img_1.thumbnail(output_size)
            img_1.save(self.image_1.path)
        if self.image_2:
            img_2 = Image.open(self.image_2.path)
            img_2.thumbnail(output_size)
            img_2.save(self.image_2.path)
        if self.image_3:
            img_3 = Image.open(self.image_3.path)
            img_3.thumbnail(output_size)
            img_3.save(self.image_3.path)
        if self.image_4:
            img_4 = Image.open(self.image_4.path)
            img_4.thumbnail(output_size)
            img_4.save(self.image_4.path)
