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

## 📂 Repository Structure

### `agents/`
- `flight_agent.py`  
- `hotel_agent.py` 
- `dining_agent.py` 
- `itinerary_agent.py` 
- TODO: _(add more agents as needed)_

### `config/`
- `llm_models.py` → Define the LLM model configuration (OpenAI / Anthropic etc.)

### `api/`
- `main.py` → FastAPI entrypoint (TODO: define routes for itinerary generation, health check, etc.)

### `graph/`
- `TravelAgent.py` → TravelAgent class using **LangGraph** (builds graph, runs workflow)

### `models/`
- `travel_model.py` → Defines `TravelState` (Pydantic model for state management)

### `tools/`
- `hotel_tools.py` → `hotel_search` function (TODO: implement API or mock)  
- `flight_tools.py` (TODO)  
- `dining_tools.py` (TODO)  
- _(add other tools as needed)_

### `tests/` (TODO)
- Unit tests for agents, tools, and graph.

### `Dockerfile` 
- Dockerize FastAPI app for deployment.

### `README.md`
- Project documentation.

---

## ✅ TODO List

- [ ] Implement tool functions (`hotel_search`, `flight_tools`, etc.)  
- [ ] Add FastAPI endpoints in `api/main.py`  
- [ ] Add unit tests in `tests/`  
- [ ] Add error handling in graph execution  
- [ ] Add `.env` handling for API keys (OpenAI, external APIs)  
- [ ] CI/CD pipeline (GitHub Actions / GitLab) (optional)  

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
