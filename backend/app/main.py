from fastapi import FastAPI

from app.api import main_router


# https://fastapi.tiangolo.com/advanced/events/#lifespan-function
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#    await database.connect()
#    yield
#    await database.disconnect()


app = FastAPI()  # lifespan=lifespan)

app.include_router(main_router)
