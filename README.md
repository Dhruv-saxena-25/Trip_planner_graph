# Trip Itinerary Planner

A conversational trip itinerary planner built with [LangGraph](https://github.com/langgraph/langgraph) and custom LangChain tools. Given a destination city, it can:

- ✅ Fetch current/future weather via **WeatherAPI**  
- ✈️ Find flight options via **Google SERP API**  
- 🏨 Find hotel options via **Google SERP API**  
- 📜 Fetch city information via LangChain’s **DuckDuckGoSearchRun**

## Prerequisites

Ensure you have UV installed. You can install UV via:

```bash
# On macOS/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows:
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or via pip:
pip install uv

# Install Python-3.12 version:
uv venv --python 3.12


# Activating the Virtual Environment
```
source .venv/bin/activate
```



## 🏗️ Architecture

