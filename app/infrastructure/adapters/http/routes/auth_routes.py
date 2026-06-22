from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.infrastructure.adapters.auth.jwt_config import (
    create_access_token,
    verify_password,
)
from app.infrastructure.adapters.database.config import get_db
from app.infrastructure.adapters.database.models import UserORM
from app.infrastructure.adapters.http.schemas.auth_schemas import Token, UserLogin

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)) -> Any:
    user = db.query(UserORM).filter(UserORM.username == payload.username).first()

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # access_token = create_access_token(data={"sub": user.username})
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.username}
    )

    return {"access_token": access_token, "token_type": "bearer"}
