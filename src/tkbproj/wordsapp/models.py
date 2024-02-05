from django.db import models
from django.utils.translation import gettext_lazy as _


class Word(models.Model):
    class Articles(models.TextChoices):
        DER = "DER", _("der")
        DIE = "DIE", _("die")
        DAS = "DAS", _("das")

    word = models.CharField(max_length=100)
    article = models.CharField(
        max_length=3,
        choices=Articles,
        default=Articles.DER,
    )
    image = models.ImageField(upload_to="word_images/")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_article_display()} {self.word}"

    def __repr__(self):
        return f"<Word id={self.id}, word={self.word} article={self.get_article_display()}>"
