# Generated by Django 3.2.9 on 2021-11-16 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='crew',
            field=models.ManyToManyField(null=True, to='movies.Crew'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='production_contries',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='runtime',
            field=models.IntegerField(null=True),
        ),
    ]
