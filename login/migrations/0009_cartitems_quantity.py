# Generated by Django 4.2.1 on 2023-06-24 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("login", "0008_cart_cartitems"),
    ]

    operations = [
        migrations.AddField(
            model_name="cartitems",
            name="quantity",
            field=models.PositiveIntegerField(blank=True, default=1, null=True),
        ),
    ]