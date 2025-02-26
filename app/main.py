from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routes import router

# Turn off redoc docs, they are useless
app = FastAPI(
    **get_settings().app_info,
    tags_metadata=get_settings().tags_metadata,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().allowed_origins,
    allow_credentials=get_settings().allowed_credentials,
    allow_methods=get_settings().allowed_methods,
    allow_headers=get_settings().allowed_headers,
)

app.include_router(router)
