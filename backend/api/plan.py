from fastapi import APIRouter,  Depends, HTTPException, status
from config.llm_models import llm
from models.travel_model import TravelState, TravelRequest
from graph.TravelAgent import TravelAgent
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from core.security import get_current_active_user, User
from core.security import UserRole
from config.redis_db import redisManager
from utilties.utils import format_travel_state_response
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
travel_agent = TravelAgent(model=llm)
graph = travel_agent.build_graph()
router = APIRouter(tags=["plan"], prefix="/api")

@router.post("/plan", response_model=None)
async def plan(
    request: TravelRequest,
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    
    id = current_user.id 
    role = current_user.role
    if role == UserRole.USER:
        subscription = current_user.subscription
        key = f"quota:{id}:"
        if (await redisManager.get_cache(key) is None):
            await redisManager.set_cache(key, subscription.quota)
            await redisManager.expire(key, 86400)  # 1 day
        else:
            quota = int(await redisManager.get_cache(key))
            print("Current quota for user", id, "is", quota)
            if quota <= 0:
                raise HTTPException(
                    status_code = status.HTTP_403_FORBIDDEN,
                    detail="Quota exceeded. Please upgrade your subscription.",
                )
            else:
                print("Decrementing quota for user:", id)
                redisManager.decr(key)
    elif role == UserRole.ADMIN:
        pass
    else:
        print("role:", role)
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail="Invalid user role.",
        )
    # Convert Pydantic request to plain dict before passing to TravelState
    travel_state = TravelState(messages=["Planning your trip..."], **request, user_id=str(id))
    
    result = await travel_agent.run(travel_state)
    
    response = format_travel_state_response(result)
    return response

