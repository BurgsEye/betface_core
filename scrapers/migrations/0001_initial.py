# Generated by Django 4.2.4 on 2023-08-29 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScraperLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scraper_name', models.CharField(max_length=255)),
                ('scraper_start_time', models.DateTimeField()),
                ('error_level', models.CharField(blank=True, max_length=255, null=True)),
                ('scraper_message', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
