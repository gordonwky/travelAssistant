from fastapi import APIRouter,  Depends, HTTPException, status
from config.llm_models import llm
from models.travel_model import TravelState, TravelRequest
from graph.TravelAgent import TravelAgent
from fastapi.security import HTTPBasic, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from typing import Annotated
from core.security import get_current_active_user, User
from core.db import User as DBUser
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
travel_agent = TravelAgent(model=llm)
graph = travel_agent.build_graph()
router = APIRouter(tags=["plan"], prefix="/api")

@router.post("/plan", response_model=None)
async def plan(
    request: TravelRequest,
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    # Convert Pydantic request to plain dict before passing to TravelState
    travel_state = TravelState(**request)
    
    result = await travel_agent.run(travel_state)
    
    return {
        "message": "Planning your trip...",
        "result": result
    }

