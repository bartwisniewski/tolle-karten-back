import os
from urllib.parse import urlparse
from urllib.request import urlretrieve

from django.conf import settings
from django.core.files import File

from ..models import Word
from .prompt_get_words import get_image, get_words


def generate_words(topic, level, old_words):
    print("generating...")
    words = get_words(topic, level, old_words)
    generated = []
    for word in words:
        if Word.objects.filter(word=word.get("word")).count() > 0:
            continue
        img_url = get_image(word=word.get("english"))
        if not img_url:
            continue
        image_name = urlparse(img_url).path.split("/")[-1]
        path = os.path.join(settings.MEDIA_ROOT, image_name)
        image = urlretrieve(url=img_url, filename=path)
        word = Word(
            word=word.get("word"),
            article=word.get("article"),
            level=level,
            tags=word.get("tags"),
        )
        word.image.save(image_name, File(open(image[0], "rb")), save=True)
        generated.append(word)
    return generated


if __name__ == "__main__":
    generated = generate_words("rośliny", "A1", [])
    for word in generated:
        print(word)
