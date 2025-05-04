from typing_extensions import TypedDict, Optional
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from serpapi import GoogleSearch
from src.state.custom_state import HotelState
import datetime
import os


def hotel_tool(llm, serp_api_keys):
# ---- Hotel Tool ----
    class HotelReport(BaseModel):
        hotel_information: str = Field(description= "A readable hotel summary")

    hotel_prompt = ChatPromptTemplate.from_messages([
        ("system", "Summarize hotel listings: {best_hotels}"),
        ("human", "Hotel info:\n\n{best_hotels}")
    ])
    structured_hotel_llm = llm.with_structured_output(HotelReport)
    hotel_report_generation = hotel_prompt | structured_hotel_llm


    # -------- Flight Summary Prompt --------
    hotel_prompt = ChatPromptTemplate.from_messages([
        ("system", """Please provide a summary of the following hotels details. Include the following information:
        Here is the best hotel information: {best_hotels} 
        - Hotel Name
        - Star Rating or Type (e.g., 5-star, boutique, hostel)
        - Approximate price per night in USDa
        - Location details (e.g., close to city center, near key landmarks, airport proximity)
        - Key amenities (e.g., Wi-Fi, breakfast, pool, gym)
        - What makes the hotel suitable or popular (e.g., great views, highly rated, walkable location)
        """),
        ("human", "Best Hotels Information:\n\n{best_hotels}")
    ])

    structured_hotel_llm = llm.with_structured_output(HotelReport)
    hotel_report_generation = hotel_prompt | structured_hotel_llm

    def hotel_finder(state: HotelState):
        q = state['city']
        check_in_date = state['start_date']
        check_out_date = state['end_date']
        search_params = {
            'api_key': serp_api_keys,
            'engine': 'google_hotels',
            'hl': 'en',
            'gl': 'us',
            'q': q,
            'check_in_date': check_in_date,
            'check_out_date': check_out_date,   
            'currency': 'USD',
            'sort_by': 8}
        search = GoogleSearch(search_params)
        results = search.get_dict()
        hotels = results['properties'][0:2]
        # Generate flight summary
        hotel_info = hotel_report_generation.invoke({"best_hotels": hotels})
        # Generate flight summary
        return {"hotel_information": hotel_info.hotel_information}
    return hotel_finder
