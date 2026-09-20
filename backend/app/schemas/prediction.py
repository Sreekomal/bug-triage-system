from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PredictionCreate(BaseModel):
    bug_id: int = Field(gt=0)
    predicted_category: str | None = Field(default=None, max_length=100)
    predicted_severity: str | None = Field(default=None, max_length=50)
    duplicate_bug: bool = False
    confidence_score: float | None = Field(default=None, ge=0.0, le=1.0)


class PredictionResponse(BaseModel):
    id: int
    bug_id: int
    predicted_category: str | None
    predicted_severity: str | None
    duplicate_bug: bool
    confidence_score: float | None
    prediction_time: datetime

    model_config = ConfigDict(from_attributes=True)