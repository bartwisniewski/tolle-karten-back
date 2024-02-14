from celery import shared_task

from .generator.generate_words import generate_words


@shared_task()
def generate_words_task(topic, level, old_words, count):
    generated = generate_words(topic, level, old_words, count)
    return generated
