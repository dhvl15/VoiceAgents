"""Caveman starter agent using Google ADK."""

from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model='gemini-2.5-flash',
    name='starter_agent',
    description="A basic helpful assistant.",
    instruction="You are a helpful assistant. Be concise and friendly.",
)
