import uuid
import streamlit as st
from datetime import date
from src.llms.llm import get_llm
from src.mail.email import email_config
from src.graph.build_graph import build_graph
import os


# ─── Page Setup
st.set_page_config(page_title="🧳 PlannyPack", layout="centered")


# ─── Make the sidebar sticky 
st.markdown(
    """
    <style>
      /* pin the sidebar container to the viewport */
      [data-testid="stSidebar"] {
        position: fixed;
        top: 0;
        left: 0;
        height: 100vh;
        overflow-y: auto;
      }
      /* push the main content over to avoid overlap */
      .css-1d391kg.e1g8pov61 {
        margin-left: 20rem;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("✈️ Smart AI Travel Concierge ")

# ─── Sidebar Intro
st.sidebar.title("📌 About This App")
st.sidebar.markdown("""
**AI Smart Travel Planner**  
Create detailed, personalized travel itineraries powered by LLMs.

🗺️ Features:
- Day-by-day trip suggestions  
- Flights and hotels  
- City info and travel tips  
- Weather-aware clothing suggestions
""")

llm = None

# ─── Sidebar LLM/API/EMAIL Configuration
st.sidebar.header("🛰️ API Configuration")

SERP_API_KEY = st.sidebar.text_input("🔍 Serp API Key", type="password")
st.sidebar.markdown("🔑 [Get Serp API Key](https://serpapi.com/dashboard)")

WEATHER_API_KEY = st.sidebar.text_input("☁️ Weather API Key", type="password")
st.sidebar.markdown("🔑 [Get Weather API Key](https://www.weatherapi.com/my/)")

# ─── Sidebar inputs 
st.sidebar.header("🤖 LLM Configuration")
provider = st.sidebar.selectbox("LLM Provider", ["Groq", "Gemini"])
model_options = {
    "Groq":   ["qwen-qwq-32b", "mistral-saba-24b", "llama-3.3-70b-versatile"],
    "Gemini": ["gemini-1.5-flash", "gemini-2.0-flash-001", "gemini-1.5-pro", "gemini-2.0-flash", "gemini-2.5-pro-preview"],
}
model_name = st.sidebar.selectbox("Model", model_options[provider])

# collect only the key you need
if provider == "Groq":
    groq_key = st.sidebar.text_input("🔗 Groq API Key", type="password")
    api_keys = {"GROQ_API_KEY": groq_key}
    st.sidebar.markdown("🔑 [Get Groq API Key](https://console.groq.com/keys)")
elif provider == "Gemini":
    google_key = st.sidebar.text_input("🔗 Gemini API Key", type="password")
    api_keys = {"GOOGLE_API_KEY": google_key}
    st.sidebar.markdown("🔑 [Get Gemini API Key](https://aistudio.google.com/app/apikey)")

st.sidebar.header("📬 EMAIL Configuration")
sender_email = st.sidebar.text_input("👤 Sender Email Id")
sender_password = st.sidebar.text_input("🛡️ Sender Password", type="password")


# ─── Initialize LLM & Graph 
llm = get_llm(provider, model_name, api_keys)
graph = build_graph(llm, SERP_API_KEY, WEATHER_API_KEY)
email_sender = email_config(sender_email, sender_password)

# ─── Main Trip Form 
with st.form("trip_form"):
    st.subheader("Enter Your Trip Details")
    user_email  = st.text_input("Enter your email")
    start_city  = st.text_input("Origin City")
    city        = st.text_input("Destination City")
    start_date  = st.date_input("Start Date", date.today())
    end_date    = st.date_input("End Date",   date.today())
    user_input  = st.text_area("Preferences", placeholder="e.g. I love historical sites and art museums.")
    submit      = st.form_submit_button("Generate Itinerary")

if submit:
    # ── Validation 
    if not (user_email and start_city and city and user_input):
        st.error("Please fill in all fields.")
    elif start_date > end_date:
        st.error("End date must be after start date.")
    else:
        with st.spinner("Planning your trip…"):
            try:
                # 1) Generate a thread for follow-ups
                thread_id = str(uuid.uuid4())
                st.session_state["thread_id"] = thread_id

                # 2) Build and send the input state
                input_state = {
                    "user_email":  user_email,
                    "start_city":  start_city,
                    "city":        city,
                    "start_date":  start_date.strftime("%Y-%m-%d"),
                    "end_date":    end_date.strftime("%Y-%m-%d"),
                    "user_input":  user_input,
                }
                plan     = graph.invoke(input_state, {"configurable": {"thread_id": thread_id}})
                response = plan.get("answer")
                result   = response.content if response else None

                if not result:
                    st.warning("No itinerary generated—please try again.")
                else:
                    # 3) Persist full context + result
                    st.session_state["input_state"] = input_state
                    st.session_state["itinerary"]   = result
                    st.session_state["recipient"]   = user_email
                    st.session_state["destination"] = city

                    st.success("Trip plan ready!")
                    st.markdown("---")
                    st.markdown(result)

            except Exception as e:
                st.error(f"Error while planning: {e}")
# ─── Follow-Up Form 
if "input_state" in st.session_state and "thread_id" in st.session_state:
    st.markdown("---")
    st.subheader("🔄 Need any tweaks?")
    with st.form("followup_form"):
        follow_up = st.text_input("Ask a follow-up question or request changes:")
        update_btn = st.form_submit_button("Update Plan")

    if update_btn and follow_up:
        with st.spinner("Re-planning…"):
            try:
                # Copy original context, swap in the new user_input
                new_state = st.session_state["input_state"].copy()
                new_state["user_input"] = follow_up

                follow_up_result = graph.invoke(
                    new_state,
                    {
                        "configurable": {"thread_id": st.session_state["thread_id"]},
                        "start_at":     "human_feedback"
                    }
                )
                resp = follow_up_result.get("answer")
                if resp:
                    # Overwrite the itinerary with the updated plan
                    st.session_state["itinerary"] = resp.content
                    st.markdown("**🔁 Updated Plan:**")
                    st.markdown(resp.content)
            except Exception as e:
                st.error(f"Error handling feedback: {e}")

# ─── Send-Email Button 
if "itinerary" in st.session_state:
    st.markdown("---")
    if st.button("📧 Approve and Send Plan to Email"):
        recipient   = st.session_state["recipient"]
        destination = st.session_state["destination"]
        result      = st.session_state["itinerary"]

        with st.spinner("Sending email…"):
            try:
                success = email_sender(
                    destination_city=destination,
                    sender_id=recipient,
                    result=result)
                st.success(f"The itinerary has been successfully sent to {recipient}.")
            except Exception as e:
                st.error(f"An error occurred while sending the email: {e}")
                success = False


