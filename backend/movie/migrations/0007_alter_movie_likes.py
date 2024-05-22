# Generated by Django 4.2.8 on 2024-05-21 00:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movie', '0006_alter_movie_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='likes',
            field=models.ManyToManyField(related_name='liked_movies', to=settings.AUTH_USER_MODEL),
        ),
    ]
