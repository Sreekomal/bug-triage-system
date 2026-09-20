from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class AIPrediction(Base):
    __tablename__ = "ai_predictions"

    id = Column(Integer, primary_key=True, index=True)

    bug_id = Column(
        Integer,
        ForeignKey("bugs.id"),
        nullable=False,
        index=True
    )

    predicted_category = Column(String(100), nullable=True)
    predicted_severity = Column(String(50), nullable=True)
    duplicate_bug = Column(Boolean, default=False, nullable=False)
    confidence_score = Column(Float, nullable=True)

    prediction_time = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    bug = relationship(
        "Bug",
        back_populates="ai_predictions"
    )