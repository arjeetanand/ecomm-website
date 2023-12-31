# Generated by Django 4.2.1 on 2023-06-26 08:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("login", "0024_remove_cart_is_paid_remove_cart_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="cart", name="is_paid", field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="cart",
            name="user",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="carts",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
