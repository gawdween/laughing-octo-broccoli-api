# Generated by Django 3.2.13 on 2022-04-17 15:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_customerprofile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customerprofile',
            old_name='profile_pic',
            new_name='image',
        ),
        migrations.RenameField(
            model_name='customerprofile',
            old_name='phone',
            new_name='phone_number',
        ),
    ]