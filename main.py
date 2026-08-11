import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if not api_key:
    raise RuntimeError("The api key is not available")


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

messages = [
    {
        "role": "user",
        "content": "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
    }
]

response = client.chat.completions.create(model="openrouter/free", messages=messages)
print("User prompt: " + messages[0]["content"])
print("Prompt tokens: " + str(response.usage.prompt_tokens))
print("Response tokens: " + str(response.usage.completion_tokens))
print("Response:")
print(response.choices[0].message.content)


