from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.database import get_db
from app.models.user import User
from app.core.security import SECRET_KEY, ALGORITHM  # ✅ берём из одного места

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")  # оставляем без /auth

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    print("TOKEN RECEIVED:", token)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False})
        user_id = int(payload.get("sub"))
        print("Decoded payload:", payload)
    except JWTError as e:
        print("TOKEN ERROR:", e)
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def role_required(allowed_roles: list):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Not authorized")
        return current_user
    return role_checker
