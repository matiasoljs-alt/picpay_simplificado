from repository.user import UserRepository
from database.models.user import Userdb
from database.session import get_session
from fastapi import Depends, HTTPException, status
from security.jwt import get_current_user_id, verify_access_token, create_access_token, refresh_access_token
from schemas.user import CreateUser, UserResponse, LoginUser, UpdateUser
from security.password import hash_password, verify_password


class UserService:

    def __init__(self, session=Depends(get_session)):
        self.user_repository = UserRepository(session)

    def create_user(self, user: CreateUser):
        try:
            existing_user = self.user_repository.findByEmail(user.email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )

            user_db = Userdb(
                name=user.name,
                email=user.email,
                password=hash_password(user.password)
            )

            return self.user_repository.create(user_db)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    def login_user(self, user: LoginUser):
        try:
            existing_user = self.user_repository.findByEmail(user.email)
            if not existing_user or not verify_password(user.password, existing_user.password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password"
                )

            access_token = create_access_token(existing_user.id)
            return {"access_token": access_token, "token_typer": "baerer"}

        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error logging in: {e}"
            )

    def showAllUsers(self):
        return self.user_repository.list_users()

    def find_user_by_id(self, user_id: int):
        return self.user_repository.find_by_id(user_id)

    def delete_user(self, user_id: int):
        user = self.user_repository.find_by_id(user_id)

        if not user:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

        self.user_repository.delete(user)

        return {"message": "User deleted successfully"}