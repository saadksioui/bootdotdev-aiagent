import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from functions.call_function import available_functions
import json


load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if not api_key:
    raise RuntimeError("The api key is not available")


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

args = parser.parse_args()
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]
response = client.chat.completions.create(
    model="openrouter/free",
    messages=messages,
    tools=available_functions
)
if args.verbose:
    print("User prompt: " + args.user_prompt)
    print("Prompt tokens: " + str(response.usage.prompt_tokens))
    print("Response tokens: " + str(response.usage.completion_tokens))
for tool_call in response.choices[0].message.tool_calls:
    function_args = json.loads(tool_call.function.arguments or "{}")
    print(f"Calling function: {tool_call.function.name}({function_args})")
print("Response:")
print(response.choices[0].message.content)


