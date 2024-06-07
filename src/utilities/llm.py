import requests
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from openai import OpenAI

from utilities.constants import (
    TOGETHER_AI_API_ENDPOINT,
    TOGETHER_AI_API_KEY,
    TOGETHER_AI_MODEL_NAME,
    FIREWORKS_API_ENDPOINT,
    FIREWORKS_API_KEY,
    FIREWORKS_MODEL_NAME,
    CLAUDE_API_ENDPOINT,
    CLAUDE_API_KEY,
    CLAUDE_MODEL_NAME,
)


def together_api_call(prompt, temperature=0.2, max_tokens=4000):
    headers = {
        "content-type": "application/json",
        "Authorization": f"Bearer {TOGETHER_AI_API_KEY}",
    }
    payload = {
        "model": TOGETHER_AI_MODEL_NAME,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "messages": [
            {
                "role": "system",
                "content": "You are a J.LEAGUE and football specialist.",
            },
            {"role": "user", "content": prompt},
        ],
    }

    try:
        req = requests.post(TOGETHER_AI_API_ENDPOINT, headers=headers, json=payload)
        req.raise_for_status()
        res = req.json()
        return None, res["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as error:
        return error, None


def fireworks_api_call(prompt, temperature=0.2, max_tokens=4000):
    headers = {
        "content-type": "application/json",
        "Authorization": f"Bearer {FIREWORKS_API_KEY}",
    }
    payload = {
        "model": FIREWORKS_MODEL_NAME,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "messages": [
            {
                "role": "system",
                "content": "You are a J.LEAGUE and football specialist.",
            },
            {"role": "user", "content": prompt},
        ],
    }

    try:
        req = requests.post(FIREWORKS_API_ENDPOINT, headers=headers, json=payload)
        req.raise_for_status()
        res = req.json()
        return None, res["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as error:
        return error, None


def get_embed_model():
    embed_model = HuggingFaceEmbedding(
        model_name="intfloat/multilingual-e5-large",
        # device="cpu",
    )
    return embed_model


def claude_api_call(prompt, temperature=0.1, max_tokens=4000):
    headers = {
        "content-type": "application/json",
        "ANTHROPIC-VERSION": "2023-06-01",
        "x-api-key": CLAUDE_API_KEY,
    }
    payload = {
        "model": CLAUDE_MODEL_NAME,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "system": "You are a J.LEAGUE and football specialist.",
        "messages": [
            {"role": "user", "content": prompt},
        ],
    }

    try:
        req = requests.post(CLAUDE_API_ENDPOINT, headers=headers, json=payload)
        req.raise_for_status()
        res = req.json()
        return None, res["content"][0]["text"]
    except requests.exceptions.RequestException as error:
        return error, None


def openai_api_call(messages, temperature=0.5):
    client = OpenAI()
    messages = [
        {
            "role": "system",
            # "content": "You are a J.LEAGUE and football commentator.",
            "content": "You are a psycologist.",
        },
        *messages,
    ]

    completion = client.chat.completions.create(
        # https://platform.openai.com/docs/models/gpt-4o
        model="gpt-4o",
        # model="gpt-4o",
        messages=messages,
    )

    result = completion.choices[0].message.content
    return result
