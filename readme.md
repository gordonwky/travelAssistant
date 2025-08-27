# Travel Assistant AI

A **full-stack AI-powered travel assistant** that generates personalized itineraries, finds flights, hotels, and dining options using a large language model (LLM) with LangChain/LangGraph tool integration. Built with FastAPI for API access and designed for parallel agent execution.  

---

## Features

- **Multi-agent architecture**: Separate agents for flights, hotels, and dining.  
- **LangChain/LangGraph integration**: Tools and commands to update state safely.  
- **Structured travel state**: Stores itinerary, flights, hotels, and dining.  
- **FastAPI server**: Provides API endpoints to query and update travel plans.  
- **Parallel-safe state updates**: Each agent updates only its own keys.  
- **Extensible**: Add more agents or tools easily (e.g., attractions, transport).  

---

## Tech Stack

- **Backend**: Python 3.13, FastAPI  
- **LLM integration**: LangChain, LangGraph  
- **Data models**: Pydantic / TypedDict  
- **Deployment-ready**: Docker-compatible  

---

## Installation

```bash
git clone https://github.com/yourusername/travel-assistant.git
cd travel-assistant
python -m venv venv
source venv/bin/activate  # Mac/Linux
# Windows: venv\Scripts\activate
pip install -r requirements.txt
