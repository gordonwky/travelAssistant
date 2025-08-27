from langgraph.graph import StateGraph, START , END

# import agents
from agents.dining_agent import dining_agent
from agents.hotel_agent import hotel_agent
from agents.flight_agent import flight_agent
from agents.itinerary_agent import itinerary_agent
from agents.validate_agent import validate_agent
# ---- State Definition ----
from models.travel_model import TravelState

# ---- Build Graph ----
def build_travel_graph():
    graph = StateGraph(TravelState)

    graph.add_node("validate", validate_agent)
    graph.add_node("itinerary", itinerary_agent)
    graph.add_node("flights", flight_agent)
    graph.add_node("dining", dining_agent)
    graph.add_node("hotels", hotel_agent)

    graph.add_edge(START,"itinerary")
    graph.add_edge(START,"flights")
    # graph.add_edge("validate", "itinerary")
    # graph.add_edge("validate", "flights")
    graph.add_edge("itinerary", "dining")
    graph.add_edge("itinerary", "hotels")
    graph.add_edge("flights",END)
    graph.add_edge("dining",END)
    graph.add_edge("hotels",END)

    return graph.compile()


# ---- Run the Graph ----
if __name__ == "__main__":
    graph = build_travel_graph()
    state = {"messages":["Plan a Tokyo trip from 20 Aug to 27 Aug"],"destination": "Tokyo","departure_date": "2023-08-20","return_date": "2023-08-27"}  # initial input
    result = graph.run(state)
    print(result["summary"])

#     # Run the agent
# if __name__ == "__main__":
#     # simplest way to call agent
#     while True:
#         message = input("You: ")
#         if message.lower() in ["q", "exit", "quit"]:
#             print("Exiting...")
#             break
#         result = hotel_agent.invoke({"messages": [("user", message)]})
#         print(result)

