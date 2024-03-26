from random import randint

from celery.result import AsyncResult, states
from django.db.models import Q
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import LEVELS_ORDER, GeneratorTask, Result, Student, Word
from .serializers import (
    GeneratorTaskSerializer,
    ResultSerializer,
    SetResultSerializer,
    StudentSerializer,
    WordSerializer,
)
from .tasks import generate_words_task


class WordList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WordSerializer
    max_words = 10

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.level = None
        self.topic = None
        self.task = None

    def get_filtered_words(self):
        self.level = self.request.GET.get("level")
        self.topic = self.request.GET.get("topic")
        words = Word.objects.all()
        if self.level and self.level in LEVELS_ORDER:
            level_index = LEVELS_ORDER.index(self.level)
            available_levels = LEVELS_ORDER[: level_index + 1]
            words = words.filter(
                level__in=available_levels
            )  # words from lower level are enabled
        if self.topic:
            words = words.filter(tags__icontains=self.topic)
        return words

    def get_new_words(self, words, results):
        return words.exclude(result__in=results).order_by("-created")[: self.max_words]

    @staticmethod
    def add_old_words(queryset, results):
        new_words_count = len(queryset)
        if new_words_count < WordList.max_words:
            max_old_words = WordList.max_words - new_words_count
            results = results.filter(rate__lt=1.0).order_by("rate", "updated")[
                :max_old_words
            ]
            word_ids = [result.word.id for result in results]
            old_words = list(Word.objects.filter(id__in=word_ids))
            queryset = list(queryset) + old_words
        return queryset

    def get_queryset(self):
        words = self.get_filtered_words()
        results = Result.objects.filter(
            Q(user=self.request.user) & Q(word__in=words)
        ).order_by("rate", "updated")
        queryset = self.get_new_words(words, results)
        queryset = self.add_old_words(queryset, results)
        if (
            self.topic
            and self.level
            and len(queryset) < self.max_words
            and not GeneratorTask.check_similiar_task_runs(topic=self.topic)
            and GeneratorTask.check_limit()
        ):
            celery_task = generate_words_task.delay(
                topic=self.topic,
                level=self.level,
                old_words=[word.word for word in words],
                count=5,
            )
            self.task = GeneratorTask.objects.create(
                user=self.request.user,
                level=self.level,
                topic=self.topic,
                job_id=celery_task.id,
            )
        return queryset

    def get(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        task_id = self.task.id if self.task else None
        response.data = {"words": response.data, "task": task_id}
        return response


class DemoList(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = WordSerializer
    max_words = 10

    def get_queryset(self):
        words = Word.objects.all().order_by("?")
        count = words.count()
        random_word = words[randint(0, count)]
        random_tag = random_word.tags.split(", ")[0]
        return Word.objects.filter(tags__icontains=random_tag)[: self.max_words]


class ResultsList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ResultSerializer
    page_size = 10

    def get_queryset(self):
        return Result.objects.filter(user=self.request.user).order_by("-updated")[
            : self.page_size
        ]


class SetResults(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SetResultSerializer

    def post(self, request, format=None):
        valid = False
        serializer = self.serializer_class(data=request.data, many=True)
        results = []
        if serializer.is_valid():
            for item in serializer.validated_data:
                word_id = item.get("word")
                word = Word.objects.get(id=word_id)
                result = item.get("result")
                result_object, created = Result.objects.get_or_create(
                    user=request.user, word=word
                )
                result_object.set_result(result)
                results.append(result_object)
                valid = True
        if valid:
            response_serializer = ResultSerializer(results, many=True)
            return Response(data=response_serializer.data, status=status.HTTP_200_OK)
        return Response(data={}, status=status.HTTP_400_BAD_REQUEST)


class StudentGetUpdate(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentSerializer

    def get_object(self):
        return Student.objects.filter(user=self.request.user).first()


def get_state(result: AsyncResult) -> any:
    try:
        return result.status
    except ValueError:
        return states.FAILURE


class GeneratorTaskGet(RetrieveAPIView):
    queryset = GeneratorTask.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = GeneratorTaskSerializer

    def get_object(self):
        obj = super().get_object()
        obj.check_state()
        return obj


class GeneratorTaskUserList(ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = GeneratorTaskSerializer

    def get_queryset(self):
        queryset = GeneratorTask.objects.filter(user=self.request.user).exclude(
            status__in=GeneratorTask.FINISHED_STATES
        )
        users_active_tasks = list(queryset)
        for task in users_active_tasks:
            state = task.check_state()
            if state in GeneratorTask.FINISHED_STATES:
                users_active_tasks.remove(task)
        return users_active_tasks
