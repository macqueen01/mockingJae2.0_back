# Generated by Django 4.1.4 on 2022-12-30 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_videomedia_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='scrolls',
            name='uploaded',
            field=models.IntegerField(default=0),
        ),
    ]