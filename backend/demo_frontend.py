# frontend_ui_only.py
import streamlit as st
from datetime import date

st.set_page_config(page_title="Travel Assistant", page_icon="🌏", layout="wide")

st.title("🌏 Travel Itinerary Planner (UI Only)")

# --- Inputs ---
destination = st.text_input("Destination", "Tokyo")
departure_date = st.date_input("Departure Date", date.today())
return_date = st.date_input("Return Date", date.today())

# --- Placeholder for itinerary ---
st.subheader("🗓️ Sample Itinerary Preview")

# Example mock data to render
sample_itinerary = [
    {
        "date": "2023-08-22",
        "morning": {"name": "Senso-ji Temple", "description": "Historic Buddhist temple"},
        "afternoon": {"name": "Tokyo Skytree", "description": "Observation tower with city views"},
        "evening": {"name": "Shinjuku Golden Gai", "description": "Nightlife district with bars"}
    },
    {
        "date": "2023-08-23",
        "morning": {"name": "Meiji Shrine", "description": "Famous Shinto shrine"},
        "afternoon": {"name": "Harajuku Takeshita Street", "description": "Trendy shopping street"},
        "evening": {"name": "Shibuya Crossing", "description": "Iconic busy intersection"}
    }
]

# Render the mock itinerary
for day in sample_itinerary:
    with st.expander(f"📅 {day['date']}"):
        st.markdown(f"**Morning**: {day['morning']['name']} - {day['morning']['description']}")
        st.markdown(f"**Afternoon**: {day['afternoon']['name']} - {day['afternoon']['description']}")
        st.markdown(f"**Evening**: {day['evening']['name']} - {day['evening']['description']}")
