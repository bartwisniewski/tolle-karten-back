import json

from .completion import chat_completion, format_messages
from .image import generate_image


def get_words(topic, level, old_words, count):
    msg = (
        f"Acting as a german language teacher from Poland generate {count} words (nouns, verbs etc.) in given topic "
        f"and on given language level. Add article [DER, DIE, DAS] as a seperate field for nouns. Add least 3 tags "
        f"including given topic to each word as a comma separated string. Topic and tags will be in polish language. "
        f"Add english and polish translation to each word. "
        f"Do not return words given in ###existing words list. The list contains german words that must not be returned"
        f"Always return array of JSON objects and nothing more. "
        f"Example prompt topic = pojazdy, level = A2 "
        f"Example response :"
        f'{{"words": [{{"word": "Auto", "article": "DAS", "tags": "pojazdy, droga, kołowe, podróż", "english": "car", '
        f'"polish" : "samochód" }}'
        f", ...]}}"
        f"###topic: {topic}"
        f"###level: {level}"
        f"###existing words: {','.join(old_words)}"
    )

    messages = format_messages([("user", msg)])
    response = chat_completion(model="gpt-3.5-turbo", messages=messages)
    try:
        response_json = json.loads(response)
    except json.JSONDecodeError:
        return None
    words = response_json.get("words")
    if not words:
        return None
    return words


def get_image(word):
    return generate_image(
        f"simple colour cartoon graphic of a {word} in a pastel colors",
        size="1024x1024",
    )


if __name__ == "__main__":
    response = get_words("rośliny", "A1", ["Baum"])
    if response:
        for word in response:
            print(word)
