# Generated by Django 4.1.10 on 2023-08-19 11:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rummage", "0005_auto_20210626_1822"),
    ]

    operations = [
        migrations.AlterField(
            model_name="searchresult",
            name="image",
            field=models.CharField(
                blank=True,
                default="https://via.placeholder.com/150.jpg",
                max_length=500,
                null=True,
            ),
        ),
    ]
