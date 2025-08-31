from fastapi import FastAPI 

from api.health_check import router as health_router
from api.plan import router as plan_router
from api.users import router as user_router
app = FastAPI()

@app.get("/")
def hello_world():
    return {"Hello World"}

app.include_router(user_router)
app.include_router(plan_router)
app.include_router(health_router)