from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Bug(Base):
    __tablename__ = "bugs"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    steps_to_reproduce = Column(Text, nullable=True)
    environment = Column(String(255), nullable=True)

    status = Column(String(50), nullable=False, default="open")

    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    assigned_to = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    creator = relationship(
        "User",
        foreign_keys=[created_by],
        back_populates="bugs_created"
    )

    assignee = relationship(
        "User",
        foreign_keys=[assigned_to],
        back_populates="bugs_assigned"
    )
    ai_predictions = relationship(
        "AIPrediction",
        back_populates="bug",
        cascade="all, delete-orphan"
    )