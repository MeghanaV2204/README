import os
from openai import OpenAI

MODEL = "openai/gpt-oss-20b"
BASE_URL = "https://api.groq.com/openai/v1"


def generate_response(messages, api_key=None):
    api_key = api_key or os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Enter a Groq API key or set the GROQ_API_KEY environment variable.")

    client = OpenAI(api_key=api_key, base_url=BASE_URL)
    response = client.responses.create(input=messages, model=MODEL)
    return response.output_text
