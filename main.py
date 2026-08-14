import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from functions.call_function import available_functions, call_function


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
for _ in range(20):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions
    )
    message = response.choices[0].message
    messages.append(message)
    if not message.tool_calls:
        print("Final response:")
        print(message.content)
        break
    for tool_call in message.tool_calls:
        result_message = call_function(
            tool_call,
            verbose=args.verbose,
        )

        messages.append(result_message)

        if args.verbose:
            print(f"-> {result_message['content']}")
    
else:
    print("Maximum iterations reached without a final response.")
    exit(1)
