# Generated by Django 4.2.1 on 2023-06-21 08:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("login", "0002_contactus"),
    ]

    operations = [
        migrations.RenameField(
            model_name="contactus", old_name="email", new_name="emailCon",
        ),
        migrations.RenameField(
            model_name="contactus", old_name="name", new_name="nameCon",
        ),
    ]
