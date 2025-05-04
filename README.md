# Trip Itinerary Planner

A conversational trip itinerary planner built with [LangGraph](https://github.com/langgraph/langgraph) and custom LangChain tools. Given a destination city, it can:

- ✅ Fetch current/future weather via **WeatherAPI**  
- ✈️ Find flight options via **Google SERP API**  
- 🏨 Find hotel options via **Google SERP API**  
- 📜 Fetch city information via LangChain’s **DuckDuckGoSearchRun**


# 🏗️ Architecture
```bash
Trip_planner_graph/
├── .env                      # Environment variables (API keys, SMTP creds)
├── .env.example              # Template for environment variables
├── .venv/                    # Python virtual environment
├── app.py                    # Application entry point
├── requirements.txt          # Project dependencies
└── src/                      # Source code
    ├── __init__.py
    ├── graph/
    │   └── built_graph.py    # LangGraph orchestration and entry point
    ├── llms/
    │   └── llms.py           # Language model configuration and wrappers
    ├── mail/
    │   └── email.py          # Email sending integration
    └── tools/
        ├── city.py           # DuckDuckGoSearchRun wrapper for city info
        ├── flight.py         # Google SERP flight search tool
        ├── hotel.py          # Google SERP hotel search tool
        └── weather.py        # WeatherAPI integration

```
# Installing Dependencies

Ensure you have UV installed. You can install UV via:

```bash
# On macOS/Linux:

curl -LsSf https://astral.sh/uv/install.sh | sh
```
```bash
# On Windows:

powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
```bash
# Or via pip:

pip install uv
```

```bash
# Install Python-3.12 version:

uv venv --python 3.12
```
```bash
# Activating the Virtual Environment

- macOS/Linux
source .venv/bin/activate
```

```bash
- Windows (PowerShell)
.venv\Scripts\Activate
```

```bash
# Installing Packages

-Single Packages
uv pip install <package_name>

- From a requirements.txt File
uv pip install -r requirements.txt
```

```bash
# Locking Dependencies

- To capture the exact versions of all installed packages, generate a lockfile:
uv lock
```


# Syncing Dependencies
- To recreate your environment elsewhere (e.g. on CI or another machine), install exactly what’s in the lockfile:

```bash
uv sync
```

