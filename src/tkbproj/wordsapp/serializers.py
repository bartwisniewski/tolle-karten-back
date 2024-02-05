from rest_framework import serializers

from .models import Word


class WordSerializer(serializers.ModelSerializer):
    article = serializers.SerializerMethodField()

    class Meta:
        model = Word
        exclude = ["created"]

    def get_article(self, obj):
        return obj.get_article_display()
