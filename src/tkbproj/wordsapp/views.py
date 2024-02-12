from django.db.models import Q
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .generator.generate_words import generate_words
from .models import Result, Student, Word
from .serializers import (
    ResultSerializer,
    SetResultSerializer,
    StudentSerializer,
    WordSerializer,
)


class WordList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WordSerializer
    max_words = 5

    def get_filtered_words(self):
        self.level = self.request.GET.get("level")
        self.topic = self.request.GET.get("topic")
        words = Word.objects.all()
        if self.level:
            words = words.filter(level=self.level)
        if self.topic:
            words = words.filter(tags__icontains=self.topic)
        return words

    def get_new_words(self, words, results):
        return words.exclude(result__in=results).order_by("-created")[: self.max_words]

    def add_old_words(self, queryset, results):
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
        if self.topic and self.level and len(queryset) < self.max_words:
            generated = generate_words(
                topic=self.topic,
                level=self.level,
                old_words=[word.word for word in words],
                count=5,
            )
            queryset = list(queryset) + generated
        return queryset


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
