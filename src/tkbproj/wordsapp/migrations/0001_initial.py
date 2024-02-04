# Generated by Django 5.0.1 on 2024-02-04 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Word",
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
                ("word", models.CharField(max_length=100)),
                (
                    "preposition",
                    models.CharField(
                        choices=[("DER", "der"), ("DIE", "die"), ("DAS", "das")],
                        default="DER",
                        max_length=3,
                    ),
                ),
                ("image", models.ImageField(upload_to="word_images/")),
                ("created", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]