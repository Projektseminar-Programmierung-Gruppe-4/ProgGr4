# Generated by Django 3.2.8 on 2022-01-04 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Forum', '0016_alter_employee_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='voteCount',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
