from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


def create_user(db: Session, user_data: UserCreate) -> User:
    existing_username = (
        db.query(User)
        .filter(User.username == user_data.username)
        .first()
    )

    if existing_username:
        raise ValueError("Username already exists")

    existing_email = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_email:
        raise ValueError("Email already exists")

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=user_data.password_hash,
        role=user_data.role,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_user(db: Session, user_id: int) -> User | None:
    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )


def get_users(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> list[User]:
    return (
        db.query(User)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_user(
    db: Session,
    user_id: int,
    user_data: UserUpdate
) -> User | None:

    user = get_user(db, user_id)

    if not user:
        return None

    update_data = user_data.model_dump(exclude_unset=True)

    if "username" in update_data:
        existing_username = (
            db.query(User)
            .filter(
                User.username == update_data["username"],
                User.id != user_id
            )
            .first()
        )

        if existing_username:
            raise ValueError("Username already exists")

    if "email" in update_data:
        existing_email = (
            db.query(User)
            .filter(
                User.email == update_data["email"],
                User.id != user_id
            )
            .first()
        )

        if existing_email:
            raise ValueError("Email already exists")

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user


def delete_user(db: Session, user_id: int) -> bool:
    user = get_user(db, user_id)

    if not user:
        return False

    db.delete(user)
    db.commit()

    return True