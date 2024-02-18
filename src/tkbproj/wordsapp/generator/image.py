import openai
from openai import OpenAI

from .settings import OPENAI_KEY


def generate_image(prompt, size):
    client = OpenAI(api_key=OPENAI_KEY)
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality="standard",
            n=1,
        )
    except openai.RateLimitError:
        return ""
    return response.data[0].url


if __name__ == "__main__":
    response = generate_image(
        "fav icon for a german words learning website", size="1024x1024"
    )
    print(response)
