# Generated by Django 4.2.4 on 2023-08-12 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tips', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipster',
            name='source',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='tipster',
            name='type',
            field=models.CharField(blank=True, choices=[('Human', 'Human'), ('Computer', 'Computer')], max_length=10, null=True),
        ),
    ]
