# Generated by Django 3.2.9 on 2021-11-22 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0012_auto_20211120_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='trailer_path',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='crews',
            field=models.ManyToManyField(related_name='movies', to='movies.Crew'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='genres',
            field=models.ManyToManyField(related_name='movies', to='movies.Genre'),
        ),
    ]
