from sqlalchemy.orm import Session

from src.db.models import User
from src.schemas.users_schema import UserModel

async def get_user_by_email(email: str, db = Session) -> User | None:
    return db.query(User).filter_by(email=email).first()

async def create_user(body: UserModel, db: Session):
    new_user = User(**body.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

async def update_token(user: User, refresh_token, db: Session):
    user.refresh_token = refresh_token
    db.commit()