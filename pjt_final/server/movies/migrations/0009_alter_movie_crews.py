# Generated by Django 3.2.9 on 2021-11-20 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0008_rename_crew_movie_crews'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='crews',
            field=models.ManyToManyField(to='movies.Crew'),
        ),
    ]