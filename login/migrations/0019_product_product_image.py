# Generated by Django 4.2.1 on 2023-06-25 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("login", "0018_delete_productimage"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="product_image",
            field=models.ImageField(blank=True, upload_to="categories"),
        ),
    ]
