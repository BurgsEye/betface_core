# Generated by Django 4.2.4 on 2023-08-12 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0007_alter_game_scores'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='game_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
