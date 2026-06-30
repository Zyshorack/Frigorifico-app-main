from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.dto.users import UserCreate, UserLogin, UserUpdate
from app.models import User
from app.repositories.domain_repository import add, get_by_id, get_user_by_username

DEMO_USERNAME = "demo"
DEMO_PASSWORD = "demo123"


def ensure_demo_user(db: Session) -> User:
    user = get_user_by_username(db, DEMO_USERNAME)
    if user is None:
        return add(
            db,
            User(
                username=DEMO_USERNAME,
                password_hash=hash_password(DEMO_PASSWORD),
                role="admin",
                is_active=True,
            ),
        )

    if user.role != "admin" or not user.is_active or not verify_password(DEMO_PASSWORD, user.password_hash):
        user.role = "admin"
        user.is_active = True
        user.password_hash = hash_password(DEMO_PASSWORD)
        db.flush()
        db.refresh(user)
    return user


def _ensure_username_available(db: Session, username: str, current_user_id: int | None = None) -> None:
    existing = get_user_by_username(db, username)
    if existing and existing.id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un usuario con ese nombre.",
        )


def _ensure_not_last_admin(db: Session, user: User) -> None:
    if user.role != "admin" or not user.is_active:
        return
    active_admins = db.scalar(
        select(func.count()).select_from(User).where(User.role == "admin", User.is_active.is_(True))
    )
    if active_admins <= 1:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede desactivar el ultimo administrador activo.",
        )


def create_user(db: Session, payload: UserCreate) -> User:
    _ensure_username_available(db, payload.username)
    user = User(
        username=payload.username,
        password_hash=hash_password(payload.password),
        role=payload.role.value,
        is_active=True,
    )
    return add(db, user)


def update_user(db: Session, user_id: int, payload: UserUpdate) -> User:
    user = get_by_id(db, User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario indicado no existe.",
        )

    changes = payload.model_dump(exclude_unset=True)
    if "username" in changes:
        _ensure_username_available(db, changes["username"], current_user_id=user.id)
        user.username = changes["username"]
    if "password" in changes and changes["password"]:
        user.password_hash = hash_password(changes["password"])
    if "role" in changes and changes["role"] is not None:
        if user.role == "admin" and changes["role"].value != "admin":
            _ensure_not_last_admin(db, user)
        user.role = changes["role"].value
    if "is_active" in changes and changes["is_active"] is not None:
        if changes["is_active"] is False:
            _ensure_not_last_admin(db, user)
        user.is_active = changes["is_active"]

    db.flush()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> None:
    user = get_by_id(db, User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario indicado no existe.",
        )
    _ensure_not_last_admin(db, user)
    user.is_active = False
    db.flush()


def delete_user_permanently(db: Session, user_id: int) -> None:
    user = get_by_id(db, User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario indicado no existe.",
        )

    _ensure_not_last_admin(db, user)

    db.delete(user)
    db.commit()


def login(db: Session, payload: UserLogin) -> User:
    user = get_user_by_username(db, payload.username)
    if user is None or not user.is_active or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contrasena incorrectos.",
        )
    return user


def list_users(db: Session) -> list[User]:
    return list(db.scalars(select(User).order_by(User.username)).all())
