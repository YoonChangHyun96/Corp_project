# Generated by Django 5.1.1 on 2024-09-18 07:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("asdf", "0005_alter_messages_connected_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="messages",
            name="connected_user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="messages",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
