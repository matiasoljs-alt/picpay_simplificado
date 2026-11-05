from fastapi import APIRouter, Depends, Request
from config.limiter import limiter
from service.user import UserService
from schemas.user import CreateUser, UserResponse, LoginUser
from database.models.user import Userdb
from security.depedencies import get_current_admin

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/create-user", response_model=UserResponse)
@limiter.limit("5/minute")
def creating_user(
    request: Request,
    user: CreateUser,
    service: UserService = Depends()
):
    return service.create_user(user)


@router.post("/login")
@limiter.limit("5/minute")
def login_user(
    request: Request,
    user: LoginUser,
    service: UserService = Depends()
):
    return service.login_user(user)


@router.get("/all-users", response_model=list[UserResponse])
@limiter.limit("30/minute")
def all_users(
    request: Request,
    service: UserService = Depends()
):
    return service.show_all_users()


@router.get("/{user_id}", response_model=UserResponse)
@limiter.limit("30/minute")
def find_user_by_id(
    user_id: int,
    request: Request,
    service: UserService = Depends()
):
    return service.find_user_by_id(user_id)


@router.delete("/{user_id}", status_code=204)
@limiter.limit("5/minute")
def delete_user(
    user_id: int,
    request: Request,
    service: UserService = Depends(),
    admin: Userdb = Depends(get_current_admin)
):
    service.delete_user(user_id)