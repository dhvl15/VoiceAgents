# AI Agents Lab

A playground for building and experimenting with AI agents using multiple model providers and agent development kits.

## Structure

```
├── google/
│   ├── .env                 # Single API key (symlinked into agents)
│   ├── tools/               # Shared custom tools
│   │   ├── __init__.py
│   │   └── finance.py       # Financial tools (yfinance)
│   ├── starter_agent/       # Basic AI news agent
│   │   ├── __init__.py
│   │   ├── .env → ../.env
│   │   └── agent.py
│   └── news_analyst/        # AI news + financial analysis agent
│       ├── __init__.py
│       ├── .env → ../.env
│       └── agent.py
├── openai/                  # OpenAI agents
│   ├── text_agent.py
│   └── voice_agent.py
├── shared/
│   └── utils.py             # Shared utilities
├── notebooks/               # Course reference notebooks
│   ├── Lesson_1.ipynb
│   └── Lesson_3.ipynb
├── .env.example             # Template for API keys
├── requirements.txt
└── README.md
```

## Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Add your Google API key (single file, shared by all Google agents)
cp .env.example google/.env
# Edit google/.env with your GOOGLE_API_KEY
```

## Providers

| Provider | SDK/ADK | Use Cases |
|----------|---------|-----------|
| Google | `google-adk` | Multi-turn agents, tool use, voice |
| OpenAI | `openai-agents` | Agents SDK, Realtime API, voice |

## Running Agents

### ADK Web UI (Official)

```bash
# Google ADK starter agent
cd google/starter_agent
adk web --port 8001

# Google ADK news analyst (with financial tools)
cd google/news_analyst
adk web --port 8002
```

### Streamlit Web App (Custom)

A custom Streamlit app for testing agents via REST API with session management:

```bash
# Start the ADK API server
cd google
adk api_server --port 8000

# In a new terminal, start the Streamlit app
streamlit run app.py
```

The Streamlit app features:
- **Session management** — create, select, and delete multiple chat sessions
- **Agent switching** — test different agents without restarting
- **Raw API response viewer** — debug agent responses
