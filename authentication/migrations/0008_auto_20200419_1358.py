# Generated by Django 2.2.10 on 2020-04-19 13:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_user_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
    ]