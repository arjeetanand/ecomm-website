# Generated by Django 4.2.1 on 2023-06-25 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("login", "0016_product_image_link"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="image_link",
            field=models.URLField(default="your_default_image_link"),
        ),
        migrations.AlterField(
            model_name="category",
            name="category_image",
            field=models.ImageField(blank=True, upload_to="categories"),
        ),
    ]
