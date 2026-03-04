from fastapi import FastAPI, Request, Header
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from routers import router as service_router

app = FastAPI(
    #title = settings.app_name,
    #description = settings.app_description,
    version = "0.0.1"
)

app.include_router(service_router)