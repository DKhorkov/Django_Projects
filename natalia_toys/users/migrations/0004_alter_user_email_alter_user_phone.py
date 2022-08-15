# Generated by Django 4.0.6 on 2022-08-14 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(error_messages={'unique': 'Пользователь с таким email уже существует.'}, max_length=254, null=True, unique=True, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(error_messages={'unique': 'Пользователь с таким номером телефона уже существует.'}, max_length=11, null=True, unique=True, verbose_name='phone number'),
        ),
    ]