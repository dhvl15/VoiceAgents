"""Basic text agent using OpenAI Agents SDK."""

import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))

import asyncio
from agents import Agent, Runner
from shared.utils import get_openai_api_key

import os
os.environ["OPENAI_API_KEY"] = get_openai_api_key()


agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant. Be concise and informative.",
    model="gpt-4o-mini",
)


async def main():
    print("OpenAI Agents SDK Basic Agent (type 'quit' to exit)\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("quit", "exit"):
            break

        result = await Runner.run(agent, user_input)
        print(f"Agent: {result.final_output}\n")


if __name__ == "__main__":
    asyncio.run(main())
