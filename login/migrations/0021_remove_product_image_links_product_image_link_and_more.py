# Generated by Django 4.2.1 on 2023-06-25 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("login", "0020_image_remove_product_image_link_product_image_links"),
    ]

    operations = [
        migrations.RemoveField(model_name="product", name="image_links",),
        migrations.AddField(
            model_name="product",
            name="image_link",
            field=models.URLField(default="your_default_image_link"),
        ),
        migrations.DeleteModel(name="Image",),
    ]
