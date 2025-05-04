# 🧳 Trip Itinerary Planner

A conversational trip itinerary planner built with [LangGraph](https://langchain-ai.github.io/langgraph/tutorials/introduction/) and custom LangChain tools. Easily plan your next trip by getting weather forecasts, flight and hotel options, and detailed city insights—all from a single, natural-language interface.

---

# 🚀 Features
- ✅ Fetch current/future weather via **WeatherAPI**  
- ✈️ Find flight options via **Google SERP API**  
- 🏨 Find hotel options via **Google SERP API**  
- 📜 Fetch city information via LangChain’s **DuckDuckGoSearchRun**

---

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
---

# ⚙️ Installing Dependencies

Ensure you have UV installed. You can install UV via:

- On macOS/Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
- On Windows

```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
- Or via pip

```bash
pip install uv
```

### Install Python-3.12 version
```bash
uv venv --python 3.12
```

### Activating the Virtual Environment 

- macOS/Linux
```bash
source .venv/bin/activate
```

- Windows (PowerShell)

```bash
.venv\Scripts\Activate
```

### Single Packages
```bash
uv pip install <package_name>
```

### From a requirements.txt File
```bash
uv pip install -r requirements.txt
```

### To capture the exact versions of all installed packages, generate a lockfile:
```bash
uv lock
```

### To recreate your environment elsewhere (e.g. on CI or another machine), install exactly what’s in the lockfile:

```bash
uv sync
```

