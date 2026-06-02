# AI Agents Lab

A playground for building and experimenting with AI agents using multiple model providers and agent development kits.

## Structure

```
├── agents/
│   ├── google_adk/      # Google Agent Development Kit experiments
│   ├── openai/          # OpenAI Agents SDK experiments
│   └── multi_provider/  # Cross-provider agent compositions
├── voice/
│   ├── google_adk/      # Voice agents with Google ADK
│   └── openai/          # Voice agents with OpenAI Realtime API
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
python agents/google_adk/basic_agent.py
python agents/openai/basic_agent.py

# Voice agent examples
python voice/google_adk/voice_agent.py
python voice/openai/voice_agent.py
```
