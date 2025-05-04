# 🧳 Trip Itinerary Planner

A conversational trip itinerary planner built with [LangGraph](https://langchain-ai.github.io/langgraph/tutorials/introduction/) and custom LangChain tools. Easily plan your next trip by getting weather forecasts, flight and hotel options, and detailed city insights—all from a single, natural-language interface.

---

# 🚀 Features

- **Weather Forecasts**  
  Fetch current and future weather via **WeatherAPI**.
- **Flight Search**  
  Discover flight options via **Google SERP API**.
- **Hotel Search**  
  Browse hotel options via **Google SERP API**.
- **City Information**  
  Retrieve detailed city data (history, attractions, travel tips) via **DuckDuckGoSearchRun**.
- **Email Notifications**  
  Send your planned trip itinerary directly to your inbox.

---

# 🏗️ Architecture
```bash
Trip_planner_graph/
├── .env
├── .venv/
├── app.py
├── requirements.txt
└── src/
    ├── __init__.py             # Package root
    ├── graph/
    │   ├── __init__.py         # Package for graph orchestration
    │   └── built_graph.py      # LangGraph entry point
    ├── llms/
    │   ├── __init__.py         # Package for LLM wrappers
    │   └── llms.py             # LLM configuration
    ├── mail/
    │   ├── __init__.py         # Package for emailing
    │   └── email.py            # Email integration
    ├── tools/
    │   ├── __init__.py         # Package for tool wrappers
    │   ├── city.py             # City info search
    │   ├── flight.py           # Flight search
    │   ├── hotel.py            # Hotel search
    │   └── weather.py          # Weather lookup
    ├── state/
    │   ├── __init__.py         # Package for app state management
    │   └── custom_state.py            # State manager module
    └── planner/
        ├── __init__.py         # Package for trip planning logic
        └── plan.py             # Plan creation module
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

