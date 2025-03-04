from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.config import get_settings, limiter
from app.routes import router

# Turn off redoc docs, they are useless
app = FastAPI(
    **get_settings().APP_INFO,
    tags_metadata=get_settings().TAG_METADATA,
    redoc_url=None,
)

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded, handler=_rate_limit_exceeded_handler
)  # type: ignore

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().ALLOWED_ORIGINS,
    allow_credentials=get_settings().ALLOWED_CREDENTIALS,
    allow_methods=get_settings().ALLOWED_METHODS,
    allow_headers=get_settings().ALLOWED_HEADERS,
)

app.include_router(prefix="/latest", router=router)
app.include_router(prefix="/v1", router=router)
