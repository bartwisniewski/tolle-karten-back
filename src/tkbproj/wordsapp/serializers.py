from rest_framework import serializers

from .models import GeneratorTask, Result, Student, Word


class WordSerializer(serializers.ModelSerializer):
    article = serializers.SerializerMethodField()

    class Meta:
        model = Word
        exclude = ["created"]

    def get_article(self, obj):
        return obj.get_article_display()


class WordListSerializer(serializers.Serializer):
    words = WordSerializer(many=True)
    task = serializers.CharField()


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        exclude = ["user"]


class ResultSerializer(serializers.ModelSerializer):
    word_word = serializers.SerializerMethodField()

    class Meta:
        model = Result
        fields = "__all__"

    def get_word_word(self, obj):
        return f"{obj.word.get_article_display()} {obj.word.word}"


class SetResultSerializer(serializers.Serializer):
    word = serializers.IntegerField(required=True)
    result = serializers.BooleanField(required=True)


class GeneratorTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratorTask
        fields = "__all__"
