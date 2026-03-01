from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=120)
    password: str = Field(min_length=8, max_length=256)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ProfileUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=120)
    interests: list[str] | None = None
    class_level: str | None = None
    target_track: str | None = None


class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str
    interests: list[str]
    class_level: str
    target_track: str


class CourseCreate(BaseModel):
    title: str = Field(min_length=2, max_length=180)
    field: str = Field(min_length=2, max_length=100)
    level: str = Field(min_length=2, max_length=60)
    objectives: list[str] = Field(default_factory=list)


class CourseRead(BaseModel):
    id: int
    title: str
    field: str
    level: str
    generated_outline: dict
    created_at: datetime


class QuizSubmit(BaseModel):
    course_id: int
    score: float = Field(ge=0, le=100)
    suspicious_actions: list[str] = Field(default_factory=list)


class QuizSubmitResponse(BaseModel):
    score: float
    flagged_cheating: bool
    message: str


class Suggestion(BaseModel):
    title: str
    reason: str
    type: str
