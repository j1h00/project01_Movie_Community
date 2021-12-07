# Generated by Django 3.2.9 on 2021-11-20 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0011_auto_20211120_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='crews',
            field=models.ManyToManyField(to='movies.Crew'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='genres',
            field=models.ManyToManyField(to='movies.Genre'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='production_countries',
            field=models.TextField(null=True),
        ),
    ]
