# Generated by Django 5.0.6 on 2024-06-23 02:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("web", "0004_alter_client_birth_date"),
    ]

    operations = [
        migrations.CreateModel(
            name="Contact",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                ("message", models.TextField()),
            ],
        ),
    ]