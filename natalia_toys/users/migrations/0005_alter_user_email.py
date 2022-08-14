# Generated by Django 4.0.6 on 2022-08-14 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_email_alter_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(default=1, error_messages={'unique': 'Пользователь с таким email уже существует.'}, max_length=254, unique=True, verbose_name='email address'),
            preserve_default=False,
        ),
    ]
