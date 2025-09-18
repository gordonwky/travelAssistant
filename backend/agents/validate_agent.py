from models.travel_model import TravelState
from config.llm_models import llm
from pydantic import BaseModel, Field
from langgraph.types import interrupt

class ValidationResult(BaseModel):
    destination: str | None = Field(default=None, description="The destination of the travel itinerary")
    departure_date: str | None = Field(default=None, description="The departure date of the travel itinerary")
    return_date: str | None = Field(default=None, description="The return date of the travel itinerary")

def validate_agent(state: TravelState) -> ValidationResult:
    """
    Validates the travel itinerary by checking key details.
    """
    # extract the last message from the chat history
    last_message = state["messages"][-1] if state["messages"] else ""
    # Create prompt for itinerary planning
    system_prompt = """
    You are a validation agent.
    Based on the message,
    check for missing or inconsistent information.
    There should be a clear destination, departure date, and return date.
    The destination should be a specific and reachable location (i.e. Mars is not a valid destination),
    departure date should be in the future and return date should be after the departure date.

    """
    result = llm.with_structured_output(ValidationResult).invoke([
        {"role":"system", "content": system_prompt},
        {"role": "user", "content": last_message}
    ])

    # Check for missing or inconsistent information
    
    if result.destination is None:
        interrupt("Missing destination information.")
    if result.departure_date is None:
        interrupt("Missing departure date information.")

    if result.return_date is None:
        interrupt("Missing return date information.")

    # Return updated state with draft itinerary
    state["itinerary"] = result  # could be raw LLM output or structured JSON if you parse it
    return state

