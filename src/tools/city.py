from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage, SystemMessage
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
from src.state.custom_state import CityState


def city_tool():
    def city_report(state: CityState):
        """Fetch information from DuckDuckGo."""
        search = DuckDuckGoSearchRun()
        try:
            response = search.invoke({"query": state['city']})
        except Exception as e:
            response = f"Error retrieving Wikipedia info: {e}"
        return {"city_information": response}
    return city_report 