from fastapi import APIRouter
from app.api.v1.endpoints import audios, auth, behavior_analysis

api_router_v1 = APIRouter()

# api_router_v1.include_router(audios.router, prefix="/audios", tags=["audios"])
api_router_v1.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router_v1.include_router(behavior_analysis.router, prefix="/behavior", tags=["behavior-analysis"])
