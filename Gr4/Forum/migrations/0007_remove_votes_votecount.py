# Generated by Django 3.2.8 on 2021-11-30 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Forum', '0006_votes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='votes',
            name='voteCount',
        ),
    ]
