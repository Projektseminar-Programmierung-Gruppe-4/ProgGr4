# Generated by Django 3.2.8 on 2022-01-04 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Forum', '0018_alter_post_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='voteCount',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]