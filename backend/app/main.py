from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.simulations import router as simulations_router

app = FastAPI(title="RESQNET API")
app.include_router(health_router, prefix="/api", tags=["health"])
app.include_router(simulations_router, prefix="/api/simulations", tags=["simulations"])
