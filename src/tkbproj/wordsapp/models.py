from django.db import models
from django.utils.translation import gettext_lazy as _


class Word(models.Model):
    class Prepositions(models.TextChoices):
        DER = "DER", _("der")
        DIE = "DIE", _("die")
        DAS = "DAS", _("das")

    word = models.CharField(max_length=100)
    preposition = models.CharField(
        max_length=3,
        choices=Prepositions,
        default=Prepositions.DER,
    )
    image = models.ImageField(upload_to="word_images/")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_preposition_display()} {self.word}"

    def __repr__(self):
        return f"<Word id={self.id}, word={self.word} prepostion={self.get_preposition_display()}>"
