from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class BugCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1)
    steps_to_reproduce: str | None = None
    environment: str | None = Field(default=None, max_length=255)
    status: str = Field(default="open", max_length=50)
    created_by: int
    assigned_to: int | None = None


class BugUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, min_length=1)
    steps_to_reproduce: str | None = None
    environment: str | None = Field(default=None, max_length=255)
    status: str | None = Field(default=None, max_length=50)
    assigned_to: int | None = None


class BugResponse(BaseModel):
    id: int
    title: str
    description: str
    steps_to_reproduce: str | None
    environment: str | None
    status: str
    created_by: int
    assigned_to: int | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)