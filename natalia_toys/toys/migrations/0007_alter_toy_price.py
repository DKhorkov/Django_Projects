# Generated by Django 4.0.6 on 2022-08-03 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toys', '0006_alter_toy_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='toy',
            name='price',
            field=models.IntegerField(help_text='Цена игрушки'),
        ),
    ]