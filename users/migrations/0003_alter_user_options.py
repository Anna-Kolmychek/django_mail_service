# Generated by Django 4.2.5 on 2023-09-22 21:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_register_key'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': [('moderator', 'can moderate mailings and users')]},
        ),
    ]
