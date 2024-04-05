# Generated by Django 5.0.4 on 2024-04-05 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_movie_description_movie_overview_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='name',
        ),
        migrations.AddField(
            model_name='movie',
            name='original_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='título original'),
        ),
        migrations.AddField(
            model_name='movie',
            name='title',
            field=models.CharField(default='', max_length=255, unique=True, verbose_name='título'),
            preserve_default=False,
        ),
    ]
