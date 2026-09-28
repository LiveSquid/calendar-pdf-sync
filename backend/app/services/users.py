from sqlalchemy.orm import Session
from app.models import User


LOCAL_USER_ID = 1

def get_local_user(db: Session) -> User:
    user = db.get(User, LOCAL_USER_ID)
    if user is None:
        user = User(id = LOCAL_USER_ID)
        db.add(user)
        db.commit()
    return user
