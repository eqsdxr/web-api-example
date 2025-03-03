from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routes import router

# Turn off redoc docs, they are useless
app = FastAPI(
    **get_settings().APP_INFO,
    tags_metadata=get_settings().TAG_METADATA,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().ALLOWED_ORIGINS,
    allow_credentials=get_settings().ALLOWED_CREDENTIALS,
    allow_methods=get_settings().ALLOWED_METHODS,
    allow_headers=get_settings().ALLOWED_HEADERS,
)

app.include_router(router)
