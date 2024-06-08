"""API for neptune"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .crud import api_router as crud_router
from .scan import api_router as scan_router
from utils import Logger

import time 

neptune_api = FastAPI(
    title="Neptune API",
    version="0.7.0",
    description="Containers SBOM & vulnerability management system",
    redoc_url=None,
    docs_url="/api",
    openapi_url="/api/openapi.json"
)

neptune_api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

neptune_api.include_router(scan_router)
neptune_api.include_router(crud_router)

http_logger = Logger("http")
@neptune_api.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    if response.status_code != 200:
        http_logger.warning("%s %s %s (%ss)",response.status_code,request.method,request.url.path,str(round(process_time,2)))
    else:
        http_logger.info("%s %s %s (%ss)",response.status_code,request.method,request.url.path,str(round(process_time,2)))

    return response

neptune_api.mount(
    path="/",
    app=StaticFiles(directory="/app/dist", html=True),
    name="ui")
