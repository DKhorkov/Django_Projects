# Generated by Django 4.0.6 on 2022-08-02 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toys', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='toy',
            name='image',
            field=models.ImageField(height_field=200, upload_to='images/', width_field=200),
        ),
    ]
