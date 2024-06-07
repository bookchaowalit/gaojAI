import os

from dotenv import load_dotenv

env = load_dotenv()

# NOTE: This is a workaround to fix the issue with the tokenizers library


# ------------------------------------------------------------
# Claude
# ------------------------------------------------------------
CLAUDE_API_ENDPOINT = os.getenv("CLAUDE_API_ENDPOINT")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
CLAUDE_MODEL_NAME = os.getenv("CLAUDE_MODEL_NAME")


# ------------------------------------------------------------
# OpenAI
# ------------------------------------------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# ------------------------------------------------------------
# Float16
# ------------------------------------------------------------
FLOAT16_API_ENDPOINT_CHAT = os.getenv("FLOAT16_API_ENDPOINT_CHAT")
FLOAT16_API_ENDPOINT_LLAMAINDEX = os.getenv("FLOAT16_API_ENDPOINT_LLAMAINDEX")
FLOAT16_API_KEY = os.getenv("FLOAT16_API_KEY")
FLOAT16_MODEL_NAME = os.getenv("FLOAT16_MODEL_NAME")


# ------------------------------------------------------------
# Fireworks
# ------------------------------------------------------------
FIREWORKS_API_ENDPOINT = os.getenv("FIREWORKS_API_ENDPOINT")
FIREWORKS_API_KEY = os.getenv("FIREWORKS_API_KEY")
FIREWORKS_MODEL_NAME = os.getenv("FIREWORKS_MODEL_NAME")


# ------------------------------------------------------------
# Fireworks
# ------------------------------------------------------------
TOGETHER_AI_API_ENDPOINT = os.getenv("TOGETHER_AI_API_ENDPOINT")
TOGETHER_AI_API_KEY = os.getenv("TOGETHER_AI_API_KEY")
TOGETHER_AI_MODEL_NAME = os.getenv("TOGETHER_AI_MODEL_NAME")


# ------------------------------------------------------------
# Database
# ------------------------------------------------------------
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
VECTOR_DB_NAME = os.getenv("VECTOR_DB_NAME")


ASSEMBLY_AI_API_KEY = os.getenv("ASSEMBLY_AI_API_KEY")


HF_EMBED_MODELS = {
    "MULTILINGUAL": {  # https://huggingface.co/intfloat/multilingual-e5-large
        "name": "intfloat/multilingual-e5-large",
        "dimensions": 1024,
        "tensor_size": 512,
    },
    "mistral": {  # https://huggingface.co/intfloat/e5-mistral-7b-instruct
        "name": "intfloat/e5-mistral-7b-instruct",
        "dimension": 1024,
        "tensor_size": 512,
    },
}
