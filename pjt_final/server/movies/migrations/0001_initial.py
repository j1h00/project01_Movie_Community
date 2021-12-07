# Generated by Django 3.2.9 on 2021-11-16 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Crew',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('role', models.CharField(max_length=20)),
                ('biography', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('original_title', models.CharField(max_length=100)),
                ('overview', models.TextField()),
                ('poster_path', models.URLField()),
                ('release_date', models.DateField()),
                ('runtime', models.IntegerField()),
                ('production_contries', models.CharField(max_length=10)),
                ('adult', models.BooleanField()),
                ('crew', models.ManyToManyField(to='movies.Crew')),
                ('genres', models.ManyToManyField(to='movies.Genre')),
            ],
        ),
    ]