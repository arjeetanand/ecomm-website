# Generated by Django 4.2.1 on 2023-07-10 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("login", "0028_remove_product_product_image_alter_cart_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="cart",
            name="razor_pay_order_id",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="cart",
            name="razor_pay_payment_id",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="cart",
            name="razor_pay_payment_signature",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]