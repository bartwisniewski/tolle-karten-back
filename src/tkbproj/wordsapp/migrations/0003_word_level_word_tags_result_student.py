# Generated by Django 5.0.1 on 2024-02-06 12:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wordsapp", "0002_rename_preposition_word_article"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="word",
            name="level",
            field=models.CharField(
                choices=[
                    ("A1", "A1"),
                    ("A2", "A2"),
                    ("B1", "B1"),
                    ("B2", "B2"),
                    ("C1", "C1"),
                    ("C2", "C2"),
                ],
                default="A1",
                max_length=2,
            ),
        ),
        migrations.AddField(
            model_name="word",
            name="tags",
            field=models.CharField(default="", max_length=200),
        ),
        migrations.CreateModel(
            name="Result",
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
                ("results", models.IntegerField(default=0)),
                (
                    "rate",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=3),
                ),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "word",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="wordsapp.word"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Student",
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
                (
                    "level",
                    models.CharField(
                        choices=[
                            ("A1", "A1"),
                            ("A2", "A2"),
                            ("B1", "B1"),
                            ("B2", "B2"),
                            ("C1", "C1"),
                            ("C2", "C2"),
                        ],
                        default="A1",
                        max_length=2,
                    ),
                ),
                ("topic", models.CharField(default="podstawy", max_length=30)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]