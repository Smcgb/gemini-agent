import argparse
import os

from dotenv import load_dotenv
from google import genai

from call_functions import available_functions
from prompts import system_prompt

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("No API Key Found")

client = genai.Client(
    api_key=api_key,
)
model = "gemini-2.5-flash"


def main():
    print("Hello from gemini-agent!")
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    user_prompt = args.user_prompt
    messages = [
        genai.types.Content(role="user", parts=[genai.types.Part(text=user_prompt)])
    ]
    response = client.models.generate_content(
        model=model,
        contents=messages,
        config=genai.types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions],
        ),
    )

    metadata = response.usage_metadata
    if args.verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {metadata.prompt_token_count}")
        print(f"Response tokens: {metadata.candidates_token_count}")

    if response.function_calls:
        for f in response.function_calls:
            print(f"Calling function: {f.name}({f.args})")
    else:
        print("Response:")
        print(response.text)


if __name__ == "__main__":
    main()
