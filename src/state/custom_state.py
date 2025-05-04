from typing_extensions import TypedDict, Optional
from pydantic import EmailStr


class FlightState(TypedDict):
        start_city: str
        city: str
        start_date: str
        end_date: str

class CityState(TypedDict):
    city: str

class HotelState(TypedDict):
        city: str
        start_date: str
        end_date: str
        
class WeatherState(TypedDict):
        city: str
        start_date: str
        end_date: str

class State(TypedDict):
    user_email: EmailStr
    start_city: str
    city: str
    start_date: str
    end_date: str
    user_input: Optional[str]
    weather_information: str
    flight_informations: str
    hotel_information: str
    city_information: str
    answer: str
    