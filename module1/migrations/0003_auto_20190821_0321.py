# Generated by Django 2.2a1 on 2019-08-20 21:51

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('module1', '0002_profile'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Profile',
            new_name='images',
        ),
    ]