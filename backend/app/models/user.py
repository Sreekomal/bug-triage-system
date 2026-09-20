from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="tester")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    bugs_created = relationship(
        "Bug",
        foreign_keys="Bug.created_by",
        back_populates="creator"
    )

    bugs_assigned = relationship(
        "Bug",
        foreign_keys="Bug.assigned_to",
        back_populates="assignee"
    )