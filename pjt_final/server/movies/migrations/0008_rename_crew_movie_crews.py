# Generated by Django 3.2.9 on 2021-11-20 05:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0007_alter_movie_crew'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='crew',
            new_name='crews',
        ),
    ]
