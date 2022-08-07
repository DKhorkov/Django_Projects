# Generated by Django 4.0.6 on 2022-08-05 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toys', '0010_alter_toy_image_1_alter_toy_image_2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='toy',
            name='is_available',
            field=models.BooleanField(default=1, help_text='Имеется в наличии?'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='toy',
            name='image_1',
            field=models.ImageField(blank=True, help_text='Изображений 1', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='toy',
            name='image_4',
            field=models.ImageField(blank=True, help_text='Изображений 4', upload_to='images/'),
        ),
    ]