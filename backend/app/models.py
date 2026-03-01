from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    full_name: str
    hashed_password: str
    role: str = Field(default="learner")
    interests: str = Field(default="")
    class_level: str = Field(default="general")
    target_track: str = Field(default="general")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Course(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    field: str = Field(index=True)
    level: str
    generated_outline: str
    owner_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class QuizAttempt(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    course_id: int = Field(foreign_key="course.id")
    score: float = 0
    flagged_cheating: bool = False
    reason: str = Field(default="")
    created_at: datetime = Field(default_factory=datetime.utcnow)
