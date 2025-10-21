# Define a flight tool with search functionality
from langchain_core.tools import tool
from typing import List
import requests

import httpx

async def get_token():
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://test.api.amadeus.com/v1/security/oauth2/token",
            data={
                "grant_type": "client_credentials",
                "client_id": AMADEUS_API_KEY,
                "client_secret": AMADEUS_API_SECRET,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        resp.raise_for_status()
        return resp.json()["access_token"]


@tool
async def flight_search(origin: str, destination: str, departure_date: str, return_date: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post("https://test.api.amadeus.com/v2/shopping/flight-offers", json={
            "origin": origin,
        "destination": destination,
        "departure_date": departure_date,
        "return_date": return_date
    })
    flights_data = response.json()
    return {"flights": flights_data}