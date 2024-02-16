import os
from urllib.parse import urlparse
from urllib.request import urlretrieve

from django.conf import settings
from django.core.files import File

from ..models import Word
from ..serializers import WordSerializer
from .prompt_get_words import get_image, get_words

ARTICLES = ["DER", "DIE", "DAS"]


def validate_word(word, topic):
    german = word.get("word")
    english = word.get("english")
    polish = word.get("polish")
    article = word.get("article", "")
    tags = word.get("tags")
    if (
        not german
        or not english
        or not polish
        or (german == english)
        or (german == polish)
        or (english == polish)
    ):
        return None

    if german.upper()[0:3] in ARTICLES:
        temp_article = german[0:3]
        word["word"] = german[4:]
        if article == "":
            article = word["article"] = temp_article.upper()

    if not (article in ARTICLES or article == ""):
        return None

    existing = Word.objects.filter(word=word.get("word")).first()
    if existing:
        if tags:
            existing.tags += ", " + tags
            existing.save()
        return None
    return word


def generate_words(topic, level, old_words, count):
    print("generating...")
    words = get_words(topic, level, old_words, count)
    generated = []
    for word in words:
        word = validate_word(word, topic)
        if not word:
            continue

        word_obj = Word(
            word=word.get("word"),
            article=word.get("article", ""),
            level=level,
            tags=word.get("tags"),
            english=word.get("english"),
            polish=word.get("polish"),
        )

        img_url = get_image(word=word_obj.english)
        if not img_url:
            continue
        image_name = urlparse(img_url).path.split("/")[-1]
        temp_path = os.path.join(settings.MEDIA_ROOT, "tmp/")
        temp_path = temp_path + str(image_name)
        image = urlretrieve(url=img_url, filename=temp_path)

        file_extension = os.path.splitext(temp_path)[1]
        word_obj.image.save(
            word_obj.word + file_extension, File(open(image[0], "rb")), save=True
        )
        generated.append(word_obj)
        if os.path.exists(temp_path):
            os.remove(temp_path)
    print("generating done")
    serializer = WordSerializer(generated, many=True)
    return serializer.data


if __name__ == "__main__":
    generated = generate_words("rośliny", "A1", [])
    for word in generated:
        print(word)
