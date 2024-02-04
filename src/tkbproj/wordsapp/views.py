from rest_framework.generics import ListAPIView

from .models import Word
from .serializers import WordSerializer


class WordList(ListAPIView):
    serializer_class = WordSerializer

    def get_queryset(self):
        return Word.objects.all()
