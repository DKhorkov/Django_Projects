# Generated by Django 4.0.6 on 2022-08-02 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toys', '0003_alter_toy_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='toy',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]