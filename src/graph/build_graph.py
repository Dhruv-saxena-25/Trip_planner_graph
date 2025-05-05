from src.tools.city import city_tool
from src.tools.flight import flight_tool
from src.tools.weather import weather_tool
from src.tools.hotel import hotel_tool
from src.planner.plan import planner, feedback
from src.state.custom_state import State
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, SystemMessage
from typing_extensions import TypedDict, Optional
from pydantic import BaseModel, Field, EmailStr
import os

def build_graph(llm, SERP_API_KEY, WEATHER_API_KEY):
    city_report = city_tool()
    get_weather_data = weather_tool(llm, WEATHER_API_KEY)
    flight_finder = flight_tool(llm, SERP_API_KEY) 
    hotel_finder = hotel_tool(llm, SERP_API_KEY)
    plan_trip = planner(llm)
    human_feedback = feedback(llm)
    
    memory = MemorySaver()
    builder = StateGraph(State)
    
    # Add nodes
    builder.add_node("city_report", city_report)
    builder.add_node("get_weather_data", get_weather_data)
    builder.add_node("flight_finder", flight_finder)
    builder.add_node("hotel_finder", hotel_finder)
    builder.add_node("plan_trip", plan_trip)
    builder.add_node("human_feedback", human_feedback)


    # edges
    builder.add_edge(START, "city_report")
    builder.add_edge(START, "get_weather_data")
    builder.add_edge(START, "flight_finder")
    builder.add_edge(START, "hotel_finder")

    builder.add_edge("city_report", "plan_trip")
    builder.add_edge("get_weather_data", "plan_trip")
    builder.add_edge("flight_finder", "plan_trip")
    builder.add_edge("hotel_finder", "plan_trip")

    def _next(state):
        return "human_feedback" if state.get("user_input") else END

    builder.add_conditional_edges("plan_trip", _next)
    builder.add_edge("human_feedback", "plan_trip")

    return builder.compile(interrupt_after=["plan_trip"], checkpointer=memory)
