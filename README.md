# AI Agents Lab

A playground for building and experimenting with AI agents using multiple model providers and agent development kits.

## Structure

```
├── google/
│   └── starter_agent/   # Google ADK starter agent
│       ├── agent.py     # Agent definition
│       └── .env         # API key configuration
├── openai/              # OpenAI agents (to be added)
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
# Google ADK starter agent
cd google/starter_agent
# Add your GOOGLE_API_KEY to .env first
adk run .
```
