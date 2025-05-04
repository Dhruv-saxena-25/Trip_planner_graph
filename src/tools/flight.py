from typing_extensions import TypedDict, Optional
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from serpapi import GoogleSearch
from src.state.custom_state import FlightState
import datetime
import os 

def flight_tool(llm, serp_api_keys):

    # ---- Flight Tool ----
    
    class IATACode(BaseModel):
        iata_code: str = Field(description="The IATA airport code for the given city. For example, Jaipur -> 'JAI', Manchester -> 'MAN'.")

    class FlightReport(BaseModel):
        flight_information: Optional[str] = Field(
            description=  "Generate paragraph of flight information summarizing the options for the given trip" # "Summary of flight options for a user’s trip."
        )

    # -------- Flight Summary Prompt --------
    flight_prompt = ChatPromptTemplate.from_messages([
        ("system", """Please provide a summary of the following flight details. Include the following information:
        Here is the best flights information: {best_flights} 
        - Flight origin and destination
        - Departure and arrival times
        - Airline(s)
        - Flight duration
        - Price information (if available)
        - Any additional notable details e.g., stopovers, flight class, etc."""),
        ("human", "Best Flights Information:\n\n{best_flights}")
    ])

    structured_flight_llm = llm.with_structured_output(FlightReport)
    flight_report_generation = flight_prompt | structured_flight_llm

    def flight_finder(state: FlightState) -> dict:
        """Help to find best flight available from sources to destination"""
        start_city = state.get("start_city")
        destination_city = state.get("city")
        start_date = state.get("start_date")
        end_date = state.get("end_date")

        # Define system prompt for IATA
        system_msg = SystemMessage(content="Provide only the three-letter IATA code for the given city in a JSON object with the key '{iata_code}'. "
        "If the city has multiple airports, choose the primary or most widely used one based on passenger traffic or common usage. "
        "For example, if the city is Jaipur, respond with {'iata_code': 'JAI'}. If the city is London, respond with {'iata_code': 'LHR'}. "
        "If the city is Manchester, respond with {'iata_code': 'MAN'}."
        "if the city has no airport give code for nearest city.")

        # Get IATA for start city
        iata_start_output = llm.with_structured_output(IATACode).invoke([
            system_msg,
            HumanMessage(content=f"What is the IATA code for {start_city}?")
        ])
        departure_iata = iata_start_output.iata_code.strip().upper()

        # Get IATA for destination city
        iata_dest_output = llm.with_structured_output(IATACode).invoke([
            system_msg,
            HumanMessage(content=f"What is the IATA code for {destination_city}?")
        ])
        arrival_iata = iata_dest_output.iata_code.strip().upper()
        if not departure_iata or not arrival_iata:
            return {"flight_report": "Could not retrieve IATA codes for the cities."}
        # Flight search via SerpAPI
        search_params = {
            "api_key": serp_api_keys,
            "engine": "google_flights",
            "hl": "en",
            "gl": "us",
            "departure_id": departure_iata,
            "arrival_id": arrival_iata,
            "outbound_date": start_date,
            "return_date": end_date,
            "currency": "USD",
        }

        # search = SerpAPIWrapper(serpapi_api_key=search_params["api_key"])
        # results = search.run(search_params)
        # print(results)
        search = GoogleSearch(search_params)
        results = search.get_dict()
        # Generate flight summary
        flight_info = flight_report_generation.invoke({"best_flights": results['best_flights']})
        return {"flight_informations": flight_info}
    return flight_finder
