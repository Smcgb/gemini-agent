import os
import argparse
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("No API Key Found")

client = genai.Client(api_key=api_key)
model='gemini-2.5-flash'

def main():
    print("Hello from gemini-agent!")
    parser = argparse.ArgumentParser(description='Chatbot')
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()
    user_prompt = args.user_prompt
    response = client.models.generate_content(model=model, contents=user_prompt)
    metadata = response.usage_metadata
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {metadata.prompt_token_count}")
    print(f"Response tokens: {metadata.candidates_token_count}")
    print(f"Response:")  
    print(response.text)

if __name__ == "__main__":
    main()
