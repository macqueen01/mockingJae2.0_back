# Generated by Django 4.1.4 on 2022-12-31 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_scrolls_uploader'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scrolls',
            name='uploader',
        ),
        migrations.AlterField(
            model_name='cell',
            name='index',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
