# Generated by Django 4.0 on 2022-01-05 00:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('Forum', '0022_subcomment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subcommentvotes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField()),
                ('dislike', models.BooleanField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
                ('subcomment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcommentvote', to='Forum.subcomment')),
            ],
        ),
    ]
