from models.travel_model import TravelState
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition 
from agents.flight_agent import flight_agent
from agents.itinerary_agent import itinerary_agent
from agents.dining_agent import dining_agent
from agents.hotel_agent import hotel_agent
from tools.hotel_tools import hotel_search
class TravelAgent:
    def __init__(self, model):
        self.model = model
        self.graph = None
    def build_graph(self):
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

        self.graph =  graph.compile()
            # Step 1: Generate itinerary
    async def run(self, user_input: TravelState):
        updated_state: TravelState = await self.graph.ainvoke(user_input)
        return updated_state