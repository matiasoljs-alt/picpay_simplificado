from sqlmodel import Session, select
from database.models.user import Userdb
from security.password import hash_password, verify_password


class UserRepository:

    def __init__(self, session: Session):
        self.session = session

    def create(self, user: Userdb):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return user

    def find_by_id(self, user_id: int):
        statement = select(Userdb).where(
            Userdb.id == user_id
        )

        return self.session.exec(statement).first()
    
    def findByEmail(self, email: str):
        statement = select(Userdb).where(
            Userdb.email == email
        )

        return self.session.exec(statement).first()

    def list_users(self):
        statement = select(Userdb)

        return self.session.exec(statement).all()

    def delete(self, user: Userdb):
        self.session.delete(user)
        self.session.commit()

    def list_users_with_low_balance(self, threshold: float):
        statement = select(Userdb).order_by(Userdb.account_balance.asc())

        return self.session.exec(statement).all()