# Generated by Django 4.0.6 on 2022-08-16 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('toys', '0002_alter_toy_options_rename_title_toy_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='toy',
            options={},
        ),
        migrations.RenameField(
            model_name='toy',
            old_name='name',
            new_name='title',
        ),
    ]