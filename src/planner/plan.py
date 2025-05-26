from langchain_core.messages import HumanMessage, SystemMessage
from src.state.custom_state import State

def planner(llm):
    # --- Final Itinerary Generator ---
    def plan_trip(state: State) -> dict:
        """Generate a comprehensive trip itinerary using the provided details and Internet context."""
        user_email = state['user_email']
        start_city = state['start_city']
        city = state["city"]
        start_date = state["start_date"]
        end_date = state["end_date"]
        user_feedback = state["user_input"]
        
        # Use the Wikipedia context if available.
        city_information = state.get("city_information", [""])[0]

        # Use weather api to get weather information
        weather_information = state.get("weather_information", [""])[0]

        # 
        flight_information = state["flight_informations"]
        
        ## Hotel Information 
        hotel_information = state.get("home_information", [''])[0]

        prompt = f"""
        You are an expert travel planner and tour guide. A user is planning a trip and has provided the following details:

        - Destination City: {city}
        - Trip Dates: From {start_date} to {end_date}
        - User Request: {user_feedback}

        Additional Context:
        1. Information about the City:
        - Brief Description about the City
        {city_information}

        2. Weather Forecast:
        - 
        {weather_information}

        The weather information should be considered in detail:
        - Daily temperature (highs and lows)
        - Conditions (sunny, cloudy, rainy, etc.)
        - Suggested clothing and gear (e.g., light clothes, umbrella, sunscreen)
        - Any impacts on travel or sightseeing (e.g., avoid outdoor sites in midday heat)

        3. Flight Details (Include at least two to three options if available):
        {flight_information}
        Each flight should include:
        - Origin and destination
        - Departure and arrival times
        - Flight Number
        - Airline(s)
        - Duration
        - Pricing (if available)
        - Any notable details (e.g., stopovers, flight class)

        4. Hotel Details (Include at least two to three options if available):
        {hotel_information}
        ** For this city, provide a list of  recommended hotels across different categories (e.g., luxury, mid-range, budget-friendly). For each hotel, include:
        - Hotel Name
        - Chrck-In and Check-Out times
        - Star Rating or Type (e.g., 5-star, boutique, hostel)
        - Approximate price per night in USD
        - Location details (e.g., close to city center, near key landmarks, airport proximity)
        - Key amenities (e.g., Wi-Fi, breakfast, pool, gym)
        - What makes the hotel suitable or popular (e.g., great views, highly rated, walkable location)
        ---

        Using all the information above, generate a detailed and engaging trip itinerary that includes the following:

        **1. Famous Places to Visit:**
        - Highlight the top attractions and landmarks in {city}.
        - Briefly explain the significance of each place.

        **2. Food Recommendations:**
        - Suggest popular food spots, local restaurants, and street food vendors.
        - Include signature dishes and local specialties that align with the user's request.

        **3. City History:**
        - Provide a brief historical overview of {city}, including key events, cultural insights, and important sites tourists can explore.

        **4. Nearby Destinations:**
        - Recommend nearby towns or attractions suitable for a short visit or day trip.
        - Explain what makes each location worth visiting and offer travel tips.

        **5. Day-by-Day Itinerary:**
        - Organize the itinerary by day (e.g., Day 1, Day 2…).
        - Include recommended activities, sightseeing spots, and food stops.
        - Integrate weather details: temperature, condition, and what to wear.
        - Add time suggestions (if applicable) and helpful local tips.
        - Acknowledge the user's input and preferences throughout the plan.
        
        **6. Estimated Overall Trip Cost:**
        - Provide an approximate breakdown of total trip costs based on:
        - Flight choice (per person)
        - Hotel accommodation (total for stay)
        - Daily food budget (estimate per day × number of days)
        - Transportation (e.g., local travel, taxis, trains)
        - Entry fees to attractions (if applicable)
        - Optional tours or excursions
        - Present a clear total cost estimate and note any possible savings or upgrades.
        - Tailor cost estimates to suit the user’s preferences (luxury, mid-range, or budget).

        
        Your goal is to deliver a trip plan that is well-organized, weather-aware, and helps the user make the most of their experience in {city} including user insput as well {user_feedback}.

        """.strip()


        response = llm.invoke([
            SystemMessage(content=prompt),
            HumanMessage(content="Please use the details above to generate a thoughtful, day-by-day travel itinerary that includes local highlights, food recommendations, and weather-specific tips.")
        ])
        return {"answer": response}
    return plan_trip 


def feedback(llm):
    # ---- Human Feedback Node ----
    def human_feedback(state: State) -> State:
        """
        Update the trip plan based on user's feedback (additional input after initial itinerary).
        It uses the previous itinerary as context and modifies it with the new request.
        """
        user_input = state.get("user_input", "")
        previous_plan = state.get("answer", "")
        city = state.get("city", "")

        if not user_input or not previous_plan:
            return {"answer": "No feedback or previous plan provided."}

        prompt = f"""
        A user provided feedback to improve or revise their travel itinerary to {city}.

        Their original plan was:
        {previous_plan}

        Their new request is:
        {user_input}

        Please revise or enhance the trip itinerary accordingly. 
        Include updates that reflect the user's feedback such as new places, food, activities, or travel tips. 
        Do not repeat the entire old plan if not necessary — only focus on the requested changes or additions.
        """

        response = llm.invoke([
            SystemMessage(content= prompt),
            HumanMessage(content="Please use the details above to generate a thoughtful, day-by-day travel itinerary that includes local highlights, food recommendations, and weather-specific tips.")
        ])

        return {"answer": response}

    return human_feedback