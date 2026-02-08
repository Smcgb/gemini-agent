import argparse
import os

from dotenv import load_dotenv
from google import genai

from call_functions import available_functions, call_function
from prompts import system_prompt


def create_client() -> genai.Client:
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("No API Key Found")
    client = genai.Client(
        api_key=api_key,
    )
    return client


def handle_function_calls(response, verbose: bool):
    function_results = []

    for f in response.function_calls:
        function_call_result = call_function(f, verbose=verbose)

        if not function_call_result.parts:
            raise Exception(f"Function call failed for {f.name}({f.args})")

        part = function_call_result.parts[0]
        func_resp = part.function_response

        if func_resp is None:
            raise Exception(f"Function call failed for {f.name}({f.args})")

        if func_resp.response is None:
            raise Exception(f"Function call failed for {f.name}({f.args})")

        function_results.append(part)

        if verbose:
            print(f"-> {func_resp.response}")

    return function_results


def main():
    print("Hello from gemini-agent!")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    client = create_client()
    model = "gemini-2.5-flash"

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
        function_results = handle_function_calls(response, verbose=args.verbose)
    else:
        print("Response:")
        print(response.text)


if __name__ == "__main__":
    main()
