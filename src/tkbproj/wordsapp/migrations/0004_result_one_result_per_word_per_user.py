# Generated by Django 5.0.1 on 2024-02-06 13:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wordsapp", "0003_word_level_word_tags_result_student"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="result",
            constraint=models.UniqueConstraint(
                fields=("user", "word"), name="one_result_per_word_per_user"
            ),
        ),
    ]
