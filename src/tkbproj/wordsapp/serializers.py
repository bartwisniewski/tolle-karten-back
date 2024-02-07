from rest_framework import serializers

from .models import Result, Student, Word


class WordSerializer(serializers.ModelSerializer):
    article = serializers.SerializerMethodField()

    class Meta:
        model = Word
        exclude = ["created"]

    def get_article(self, obj):
        return obj.get_article_display()


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        exclude = ["user"]


class ResultSerializer(serializers.ModelSerializer):
    word_word = serializers.CharField(source="word.word")

    class Meta:
        model = Result
        fields = "__all__"


class SetResultSerializer(serializers.Serializer):
    word = serializers.IntegerField(required=True)
    result = serializers.BooleanField(required=True)
