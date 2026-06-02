# AI Agents Lab

A playground for building and experimenting with AI agents using multiple model providers and agent development kits.

## Structure

```
├── google/
│   ├── text_agent.py    # Google ADK text agent
│   └── voice_agent.py   # Google voice agent (placeholder)
├── openai/
│   ├── text_agent.py    # OpenAI Agents SDK text agent
│   └── voice_agent.py   # OpenAI voice agent (placeholder)
├── shared/
│   └── utils.py         # Shared utilities, config loading
├── .env.example         # Template for API keys
├── requirements.txt     # Python dependencies
└── README.md
```

## Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy env template and add your API keys
cp .env.example .env
```

## Providers

| Provider | SDK/ADK | Use Cases |
|----------|---------|-----------|
| Google | `google-adk` | Multi-turn agents, tool use, voice |
| OpenAI | `openai-agents` | Agents SDK, Realtime API, voice |

## Running Agents

```bash
# Text agent examples
python google/text_agent.py
python openai/text_agent.py

# Voice agent examples
python google/voice_agent.py
python openai/voice_agent.py
```
