# frontend_ui_only.py
import streamlit as st
from datetime import date
import time 
import requests
API_BASE = "http://localhost:8000"  # replace with your backend UR
from shared.models.travel_model import TravelRequest

def travel_dashboard():
    # st.set_page_config(page_title="Travel Assistant", page_icon="🌏", layout="wide")

    st.title("🌏 Travel Itinerary Planner")

    # --- Inputs ---
    origin = st.text_input("Origin", "New York")
    destination = st.text_input("Destination", "Tokyo")
    departure_date = st.date_input("Departure Date", date.today())
    return_date = st.date_input("Return Date", date.today())

    st.title("Trip Planner (Simulation)")

    # --- Fake TravelState ---
    # travel_state = {
    #     "flight": {
    #         "airline_name": "Cathay Pacific",
    #         "flight_number": "CX524",
    #         "departure_airport": "HKG",
    #         "arrival_airport": "HND",
    #         "departure_time": "2025-09-15T09:00:00+08:00",
    #         "arrival_time": "2025-09-15T14:20:00+09:00",
    #         "return_departure_time": "2025-09-18T15:20:00+09:00",
    #         "return_arrival_time": "2025-09-18T19:10:00+08:00",
    #         "price": 3880.0,
    #         "currency": "HKD",
    #         "seat_class": "Economy",
    #         "stops": 0,
    #         "duration": "8h 10m"
    #     },
    #     "itinerary": [
    #         {
    #             "date": "2025-09-15",
    #             "morning": None,
    #             "afternoon": "Explore Asakusa district: Sensō-ji Temple and Nakamise shopping street for traditional culture and souvenirs.",
    #             "evening": "Walk along Sumida River and enjoy Tokyo Skytree views or visit the observation deck."
    #         },
    #         {
    #             "date": "2025-09-16",
    #             "morning": "Stroll through Ueno Park and explore the Tokyo National Museum.",
    #             "afternoon": "Discover Akihabara for electronics, anime, and pop culture shopping.",
    #             "evening": "Wander through Shibuya to experience the famous crossing and Hachiko statue."
    #         },
    #         {
    #             "date": "2025-09-17",
    #             "morning": "Visit Meiji Shrine in Harajuku, then explore Takeshita Street for youth culture and fashion.",
    #             "afternoon": "Relax at Shinjuku Gyoen National Garden and visit nearby department stores in Shinjuku.",
    #             "evening": "Enjoy the vibrant lights and atmosphere of Kabukicho or Omoide Yokocho in Shinjuku."
    #         },
    #         {
    #             "date": "2025-09-18",
    #             "morning": "Visit the Imperial Palace East Gardens for a serene walk and some history.",
    #             "afternoon": None,
    #             "evening": None
    #         }
    #     ],
    #     "dining": [
    #         {
    #             "date": "2025-09-15",
    #             "morning": {"name": "Andon Ryokan Cafe", "cuisine": "Japanese (Light Breakfast)", "location": "Near Minowa Station, Taito", "price_range": "$", "rating": 4.4},
    #             "afternoon": {"name": "Asakusa Menchi", "cuisine": "Japanese (Katsu & Menchi Katsu)", "location": "Nakamise Shopping Street, Asakusa", "price_range": "$", "rating": 4.2},
    #             "evening": {"name": "BREW La La", "cuisine": "Western/Japanese Bar Food", "location": "Sumida Riverside, close to Tokyo Skytree", "price_range": "$$", "rating": 4.3}
    #         },
    #         {
    #             "date": "2025-09-16",
    #             "morning": {"name": "Ueno 3153 Café", "cuisine": "Japanese/Western Café", "location": "Across from Ueno Park entrance, Ueno", "price_range": "$", "rating": 4.1},
    #             "afternoon": {"name": "Akihabara Gyu-Katsu Ichi Ni San", "cuisine": "Japanese (Beef Cutlet)", "location": "Akihabara", "price_range": "$$", "rating": 4.5},
    #             "evening": {"name": "Uobei Shibuya Dogenzaka", "cuisine": "Japanese (Conveyor Belt Sushi)", "location": "Shibuya, near the Crossing", "price_range": "$", "rating": 4.2}
    #         },
    #         {
    #             "date": "2025-09-17",
    #             "morning": {"name": "Afuri Harajuku", "cuisine": "Japanese (Ramen)", "location": "Near Takeshita Street, Harajuku", "price_range": "$$", "rating": 4.4},
    #             "afternoon": {"name": "Tsunahachi Shinjuku", "cuisine": "Japanese (Tempura)", "location": "Shinjuku", "price_range": "$$", "rating": 4.5},
    #             "evening": {"name": "Kabukicho Yokocho", "cuisine": "Japanese (Izakaya Alley - Multiple Food Stalls)", "location": "Kabukicho, Shinjuku", "price_range": "$$", "rating": 4.3}
    #         },
    #         {
    #             "date": "2025-09-18",
    #             "morning": {"name": "Marunouchi Café SEEK", "cuisine": "Japanese/Western Café", "location": "Marunouchi near Tokyo Station", "price_range": "$", "rating": 4.0},
    #             "afternoon": {"name": "Kajitsuen Marunouchi", "cuisine": "Japanese (Fruit Parlor & Light Lunch)", "location": "Marunouchi Bldg., Tokyo Station area", "price_range": "$$", "rating": 4.3},
    #             "evening": {"name": "Soranoiro Nippon", "cuisine": "Japanese (Creative Ramen)", "location": "Tokyo Ramen Street, Tokyo Station", "price_range": "$", "rating": 4.2}
    #         }
    #     ]
    # }

    # --- Submit button ---
    if st.button("Plan Trip"):
        access_token = st.session_state.token
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        travel_request = TravelRequest(
            origin=origin,
            destination=destination,
            departure_date=str(departure_date),
            return_date=str(return_date),
        )
        # print("Token:", access_token)
        st.info("Planning your trip... ⏳")

        try:
            resp = requests.post(f"{API_BASE}/api/plan", json=travel_request, headers=headers)
            if resp.status_code == 200:
                travel_state = resp.json()
                print("Trip planned:", travel_state)

            else:
                st.error(resp.json().get("detail", "Login failed"))
        except Exception as e:
            st.error(f"Error connecting to backend: {e}")
        time.sleep(2)  # simulate backend processing
        st.success("Trip planned successfully!")

        # --- Flight ---
        f = travel_state["flight"]
        st.subheader("✈️ Flight Details")
        st.markdown(f"**Airline**: {f['airline_name']} ({f['flight_number']})")
        st.markdown(f"**From**: {f['departure_airport']} → **To**: {f['arrival_airport']}")
        st.markdown(f"**Departure / Return**: {f['departure_time']} → {f['return_departure_time']}")
        st.markdown(f"**Price**: {f['price']} {f['currency']} | **Seat**: {f['seat_class']}")

        # --- Hotel ---
        st.subheader("🏨 Hotel Itinerary")
        for day in travel_state["hotel"]["itinerary"]:
            with st.expander(f"📅 {day['date']}"):
                st.markdown(f"**Hotel Name**: {day['name']}")
                st.markdown(f"**Location**: {day['location']}")
                st.markdown(f"**Check-in**: {day['check_in']}")
                st.markdown(f"**Check-out**: {day['check_out']}")
                st.markdown(f"**Price**: {day['price']} {day['currency']}")

        # --- Dining ---
        st.subheader("🍽️ Dining Plan")
        for day in travel_state["dining"]["meals"]:
            with st.expander(f"📅 {day['date']}"):
                for period in ["morning", "afternoon", "evening"]:
                    item = day.get(period)
                    if item:
                        # note: restaurant_name instead of name
                        st.markdown(
                            f"**{period.capitalize()}**: {item['restaurant_name']} "
                            f"({item['cuisine']}) - {item['location']} | "
                            f"Price: {item['price_range']}, Rating: {item['rating']}"
                        )

        # --- Itinerary ---
        st.subheader("🗓️ Daily Spots")
        for day in travel_state["itinerary"]["spots"]:
            with st.expander(f"📅 {day['date']}"):
                for period in ["morning", "afternoon", "evening"]:
                    spot = day.get(period)
                    if spot:
                        st.markdown(f"**{period.capitalize()}**: {spot}")

    