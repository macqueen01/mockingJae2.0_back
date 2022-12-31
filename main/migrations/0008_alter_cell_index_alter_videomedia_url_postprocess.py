# Generated by Django 4.1.4 on 2022-12-31 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0007_remove_scrolls_uploader_alter_cell_index"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cell",
            name="index",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="videomedia",
            name="url_postprocess",
            field=models.TextField(default="", null=True),
        ),
    ]
