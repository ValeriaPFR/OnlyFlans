# Generated by Django 5.0.6 on 2024-06-22 02:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("web", "0003_alter_client_groups_alter_client_user_permissions"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="birth_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
