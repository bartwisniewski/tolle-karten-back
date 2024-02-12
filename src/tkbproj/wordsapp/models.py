from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()

LEVELS = {
    "A1": "A1",
    "A2": "A2",
    "B1": "B1",
    "B2": "B2",
    "C1": "C1",
    "C2": "C2",
}


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
    level = models.CharField(
        max_length=2,
        choices=LEVELS,
        default="A1",
    )
    tags = models.CharField(max_length=200, default="")
    created = models.DateTimeField(auto_now_add=True)

    @property
    def tags_list(self):
        return self.tags.split(", ")

    def __str__(self):
        return f"{self.get_article_display()} {self.word}"

    def __repr__(self):
        return f"<Word id={self.id}, word={self.word} article={self.get_article_display()}>"


class Student(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.CharField(
        max_length=2,
        choices=LEVELS,
        default="A1",
    )
    topic = models.CharField(max_length=30, default="podstawy")


def create_student(sender, user, request, **kwargs):
    try:
        user.student
    except User.student.RelatedObjectDoesNotExist:
        Student.objects.create(user=user)


user_logged_in.connect(create_student)


class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    results = models.IntegerField(default=0)
    rate = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "word"], name="one_result_per_word_per_user"
            )
        ]

    def calc_rate(self) -> None:
        r = self.results
        wages = [5, 3, 2, 1, 1]
        normed = [wage / sum(wages) for wage in wages]
        rate = 0.0
        for i in range(5):
            if r & (pow(2, i)):
                rate += normed[i]
        self.rate = rate

    def set_result(self, result: bool) -> None:
        self.results = self.results << 1
        if result:
            self.results += 1  # it means bit 0 will be set, so last result is OK
        if self.results > 255:
            self.results = self.results % 256
        self.calc_rate()
        self.save()
