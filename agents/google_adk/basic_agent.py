"""Basic text agent using Google ADK."""

import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2]))

from google import genai
from google.genai import types
from shared.utils import get_google_api_key


def main():
    client = genai.Client(api_key=get_google_api_key())

    print("Google ADK Basic Agent (type 'quit' to exit)\n")

    history = []

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("quit", "exit"):
            break

        history.append(types.Content(role="user", parts=[types.Part(text=user_input)]))

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=history,
        )

        assistant_text = response.text
        print(f"Agent: {assistant_text}\n")

        history.append(types.Content(role="model", parts=[types.Part(text=assistant_text)]))


if __name__ == "__main__":
    main()
