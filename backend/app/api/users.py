from fastapi import APIRouter

from app.core.schemas import UserResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")#, response_model=MultipleUsers)
def read_users():
    return {"users": "only u"}


@router.post("/", response_model=UserResponse)
def create_user():
    pass


@router.put("/")
def update_user():
    pass


@router.delete("/")
def delete_user():
    pass
