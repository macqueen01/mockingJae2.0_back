# Generated by Django 4.1.4 on 2022-12-30 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_cell'),
    ]

    operations = [
        migrations.AddField(
            model_name='videomedia',
            name='title',
            field=models.CharField(default='Untitled', max_length=400),
        ),
    ]
