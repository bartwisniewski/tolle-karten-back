from datetime import datetime, timedelta

from celery.result import AsyncResult, states
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

LEVELS_ORDER = ["A1", "A2", "B1", "B2", "C1", "C2"]


class Word(models.Model):
    class Articles(models.TextChoices):
        DER = "DER", _("der")
        DIE = "DIE", _("die")
        DAS = "DAS", _("das")

    word = models.CharField(max_length=100)
    polish = models.CharField(max_length=100, default="")
    english = models.CharField(max_length=100, default="")
    article = models.CharField(
        max_length=3,
        choices=Articles,
        default=Articles.DER,
        blank=True,
        null=True,
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
        article = self.get_article_display() + " " if self.article else ""
        return f"{article}{self.word}"

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

    def __str__(self):
        return f"{self.user} | {self.level} | {self.topic}"

    def __repr__(self):
        return f"<Student {self.id} user_id={self.user.id}, level={self.level} topic={self.topic}>"


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

    def __str__(self):
        return f"{self.user} - {self.word}, wynik: {self.results} | {self.rate}"

    def calc_rate(self) -> None:
        r = self.results
        wages = [34, 21, 13, 8, 5, 3, 2, 1]
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


class GeneratorTask(models.Model):
    FINISHED_STATES = [states.FAILURE, states.SUCCESS]
    LIMIT = 5
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    level = models.CharField(
        max_length=2,
        choices=LEVELS,
        default="A1",
    )
    topic = models.CharField(max_length=30, default="podstawy")
    job_id = models.CharField(max_length=100)
    status = models.CharField(max_length=10, default=states.PENDING)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} wygenerował "{self.topic}", zadanie: {self.job_id}-{self.status}'

    def check_state(self) -> any:
        result = AsyncResult(id=self.job_id)
        try:
            self.status = result.status
        except ValueError:
            self.status = states.FAILURE
        self.save()
        return self.status

    @staticmethod
    def check_similiar_task_runs(topic):
        tasks = GeneratorTask.objects.filter(topic__contains=topic).exclude(
            status__in=GeneratorTask.FINISHED_STATES
        )
        for task in tasks:
            state = task.check_state()
            if state not in GeneratorTask.FINISHED_STATES:
                return True
        return False

    @staticmethod
    def check_limit():
        startdate = datetime.now() - timedelta(hours=1)
        tasks_count = GeneratorTask.objects.filter(created__gte=startdate).count()
        return tasks_count < GeneratorTask.LIMIT
