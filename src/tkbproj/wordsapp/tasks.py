from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded

from .generator.generate_words import generate_words


@shared_task(time_limit=240)
def generate_words_task(topic, level, old_words, count):
    try:
        generated = generate_words(topic, level, old_words, count)
        return generated
    except SoftTimeLimitExceeded:
        pass
