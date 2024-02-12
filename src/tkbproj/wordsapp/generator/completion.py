from openai import OpenAI, RateLimitError

from .settings import OPENAI_KEY


def format_messages(messages):
    return [{"role": message[0], "content": message[1]} for message in messages]


def chat_completion(model, messages):
    client = OpenAI(api_key=OPENAI_KEY)
    try:
        response = client.chat.completions.create(model=model, messages=messages)
    except RateLimitError:
        return ""
    return response.choices[0].message.content


def stream_response(response):
    for chunk in response.iter_content(chunk_size=1024):
        print(chunk.decode(), end="")


def stream_completion(model, messages):
    client = OpenAI(api_key=OPENAI_KEY)
    completion = client.chat.completions.create(model=model, messages=messages)
    if completion["code"] == 200:
        # Stream and display the response content
        stream_response(completion["choices"][0]["message"]["content"])
    else:
        print("Request failed with status code:", completion["code"])
