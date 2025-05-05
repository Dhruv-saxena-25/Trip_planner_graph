from typing_extensions import TypedDict, Optional
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from src.state.custom_state import WeatherState
import datetime
import requests
import os 

def weather_tool(llm, WEATHER_API_KEY):
    # ---- Weather Tool ----
    class WeatherRport(BaseModel):
        weather_information: str = Field(description="Give the detailed weather information report for the given city.")

    # LLM with function call
    structured_weather_llm = llm.with_structured_output(WeatherRport)

    ## Prompt
    system = """
    Generate a detailed weather report for the given city using the weather data provided.
    Your output should be a natural language paragraph summarizing the weather for each day, including key details like the condition, high and low temperatures, and precipitation.
    Return your answer as valid JSON with the following format:
    {{
    "weather_information": "Your generated report paragraph..."
    }}
    """
    response = ChatPromptTemplate.from_messages(
        [
            ('system', system),
            ("human", "Wether Information: \n\n {weather_results}")
        ]
    )
    weather_report_generation = response | structured_weather_llm

    def get_weather_data(state: WeatherState):
        """
        Retrieve weather data for all dates between start_date and end_date for a given city using WeatherAPI.
        
        Parameters:
        - start_date (str): The starting date in YYYY-MM-DD format.
        - end_date (str): The ending date in YYYY-MM-DD format.
        - city (str): The city for which weather information is requested.
        
        Returns:
        - dict: A dictionary with keys as date strings and values as weather data or error messages.
        """
        try:
            city=  state['city']
            start = state['start_date']
            end = state['end_date']

            
            start = datetime.datetime.strptime(start, "%Y-%m-%d").date()
            end = datetime.datetime.strptime(end, "%Y-%m-%d").date()
        except ValueError:
            return {"error": "Invalid date format. Please use YYYY-MM-DD for both start_date and end_date."}
        
        if end < start:
            return {"error": "end_date must be the same or after start_date."}
        
        weather_results = {}
        today = datetime.date.today()
        total_days = (end - start).days + 1

        for i in range(total_days):
            current_date = start + datetime.timedelta(days=i)
            current_date_str = current_date.strftime("%Y-%m-%d")
            delta_days = (current_date - today).days

            # If the date is in the past, record an error message for that date.
            if delta_days < 0:
                weather_results[current_date_str] = "The entered date is in the past."
                continue
            # Use forecast.json for dates within the next 14 days (including today).
            elif delta_days <= 14:
                no_of_days = delta_days + 1
                url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={city}&days={no_of_days}&aqi=no&alerts=no"
            # Use future.json for dates between 15 and 299 days in the future.
            elif delta_days < 300:
                url = f"http://api.weatherapi.com/v1/future.json?key={WEATHER_API_KEY}&q={city}&dt={current_date_str}"
            else:
                weather_results[current_date_str] = "The entered date is too far in the future. Please enter a date less than 300 days from today."
                continue
            
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                
                # Extract the weather data.
                # For forecast.json, search for the matching forecast day.
                if delta_days <= 14:
                    forecast_days = data.get('forecast', {}).get('forecastday', [])
                    forecast_for_date = next((day.get("day", "No day info available.") for day in forecast_days if day.get("date") == current_date_str), None)
                    if forecast_for_date:
                        weather_results[current_date_str] = forecast_for_date
                    else:
                        weather_results[current_date_str] = "Forecast data not found for this date."
                else:
                    # For future.json endpoint, assume the first (and only) forecast day is the target.
                    forecast_days = data.get('forecast', {}).get('forecastday', [])
                    if forecast_days:
                        weather_results[current_date_str] = forecast_days[0].get("day", "No day info available.")
                    else:
                        weather_results[current_date_str] = "Weather data not found."
            except requests.RequestException as e:
                weather_results[current_date_str] = f"Request failed: {e}"
        weather_information= weather_report_generation.invoke({"weather_results": weather_results})
        return {"weather_information": weather_information.weather_information}
    return get_weather_data