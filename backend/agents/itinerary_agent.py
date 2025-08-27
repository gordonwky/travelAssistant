from typing import Annotated, List
from typing_extensions import TypedDict
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from config.llm_models import llm
from models.travel_model import TravelState
from models.itinerary_model import SpotList
from langchain_core.messages import ToolMessage
from agents.dining_agent import dining_agent
from agents.flight_agent import flight_agent
from agents.hotel_agent import hotel_agent
from langgraph.prebuilt import ToolNode, tools_condition 
from tools.hotel_tools import hotel_search
# @tool
# def search_spots():
#     pass

def itinerary_agent(state: TravelState):
    """
    Generates a draft itinerary based on destination and dates.
    Uses an LLM bound with search tools (e.g., search_spots).
    """

    # Bind tools (e.g., search spots, local attractions)
    # model_with_tools = llm.bind_tools([search_spots])
    model_with_tools = llm.with_structured_output(SpotList)
    # Extract info from state
    destination = state["destination"]
    departure_date = state["departure_date"]
    return_date = state["return_date"]
    flight = state["flight"]
    # Create prompt for itinerary planning
    system_prompt = f"""
    You are a Spots Planner AI.
    Based on the destination '{destination}' and dates '{departure_date} - {return_date}',
    consider the flight details: {flight}, save buffer travel time for the flight.
    Using this information, create a day-by-day itinerary draft.
    Suggest key attractions, districts, and activities for each day for morning, afternoon, and evening.
    Do not include any transportation details, dining suggestions, or accommodation recommendations.
    Keep in mind travel time between spots and variety.

    """

    # Invoke model
    result = model_with_tools.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Please plan my trip to {destination} from {departure_date} to {return_date}."}
    ])
    print("Itinerary Result:", result)
    # Return updated state with draft itinerary
    state["itinerary"] = result  
    # could be raw LLM output or structured JSON if you parse it
    return state



# ---- Build Graph ----
def build_travel_graph():
    graph = StateGraph(TravelState)
    graph.add_node("flight", flight_agent)
    graph.add_node("itinerary", itinerary_agent)
    graph.add_node("dining", dining_agent)
    graph.add_node("hotel", hotel_agent)


    graph.add_edge(START,"flight")
    graph.add_edge("flight","itinerary")
    graph.add_edge("itinerary","dining")
    graph.add_edge("itinerary","hotel")

    hotel_tool_node = ToolNode(tools=[hotel_search])
    graph.add_node("tools", hotel_tool_node)

    graph.add_conditional_edges(
        "hotel",
        tools_condition,
)
    graph.add_edge("tools", "hotel")
    graph.add_edge("hotel",END)
    # graph.add_edge("dining",END)

    return graph.compile()


def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}], "origin": "Hong Kong",
                               "destination": "Tokyo","departure_date": "2025-08-22","return_date": "2025-08-27"}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)

# ---- Run the Graph ----
if __name__ == "__main__":
    graph = build_travel_graph()

    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
    else:
        result = graph.invoke(TravelState(
            messages=[{"role": "user", "content": user_input}],
            origin="Hong Kong",
            destination="Tokyo",
            departure_date="2025-08-22",
            return_date="2025-08-27",
        ))
        print("===== Final Graph State =====")
        # final_state is a dict with all keys in your TravelState
        for key, value in result.items():
            print(f"{key}: {value}")

