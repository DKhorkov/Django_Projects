# Generated by Django 4.0.6 on 2022-08-02 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toys', '0002_alter_toy_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='toy',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]