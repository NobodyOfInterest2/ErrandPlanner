# Generated by Django 4.1.6 on 2023-03-23 16:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Errand",
            fields=[
                ("id", models.SmallIntegerField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=20)),
                ("priority", models.SmallIntegerField()),
                ("streetaddr", models.CharField(max_length=30)),
                ("city", models.CharField(max_length=20)),
                ("state", models.CharField(max_length=2)),
                ("zip", models.SmallIntegerField()),
                ("start", models.DateTimeField(blank=True)),
                ("end", models.DateTimeField(blank=True)),
                ("duration", models.DurationField(blank=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "id")},
            },
        ),
    ]
