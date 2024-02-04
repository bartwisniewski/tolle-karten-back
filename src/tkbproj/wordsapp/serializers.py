from rest_framework import serializers

from .models import Word


class WordSerializer(serializers.ModelSerializer):
    preposition = serializers.SerializerMethodField()

    class Meta:
        model = Word
        exclude = ["created"]

    def get_preposition(self, obj):
        return obj.get_preposition_display()
