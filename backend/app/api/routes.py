import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.api.deps import get_current_user
from app.core.database import get_session
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models import Course, QuizAttempt, User
from app.schemas import (
    CourseCreate,
    CourseRead,
    ProfileUpdate,
    QuizSubmit,
    QuizSubmitResponse,
    Suggestion,
    Token,
    UserLogin,
    UserRead,
    UserRegister,
)
from app.services.course_generator import build_course_outline

router = APIRouter(prefix="/api/v1")
PROCTORING_SIGNALS = {"copy", "paste", "tab-switch", "camera-off"}


def _interests_to_list(interests: str) -> list[str]:
    return [item for item in interests.split(",") if item]


def _serialize_user(user: User) -> UserRead:
    return UserRead(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        interests=_interests_to_list(user.interests),
        class_level=user.class_level,
        target_track=user.target_track,
    )


def _serialize_course(course: Course) -> CourseRead:
    return CourseRead(
        id=course.id,
        title=course.title,
        field=course.field,
        level=course.level,
        generated_outline=json.loads(course.generated_outline),
        created_at=course.created_at,
    )


@router.post("/auth/register", response_model=Token)
def register_user(payload: UserRegister, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.email == payload.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=payload.email,
        full_name=payload.full_name.strip(),
        hashed_password=get_password_hash(payload.password),
    )
    session.add(user)
    session.commit()
    return Token(access_token=create_access_token(payload.email))


@router.post("/auth/login", response_model=Token)
def login_user(payload: UserLogin, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == payload.email)).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return Token(access_token=create_access_token(user.email))


@router.get("/users/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)):
    return _serialize_user(current_user)


@router.patch("/users/me", response_model=UserRead)
def update_me(
    payload: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    updates = payload.model_dump(exclude_none=True)

    if "interests" in updates:
        normalized = [interest.strip() for interest in updates.pop("interests") if interest.strip()]
        current_user.interests = ",".join(dict.fromkeys(normalized))

    for key, value in updates.items():
        setattr(current_user, key, value.strip() if isinstance(value, str) else value)

    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return _serialize_user(current_user)


@router.post("/courses", response_model=CourseRead)
def create_course(
    payload: CourseCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    outline = build_course_outline(payload.title, payload.field, payload.level, payload.objectives)
    course = Course(
        title=payload.title.strip(),
        field=payload.field.strip(),
        level=payload.level.strip(),
        generated_outline=json.dumps(outline),
        owner_id=current_user.id,
    )
    session.add(course)
    session.commit()
    session.refresh(course)
    return _serialize_course(course)


@router.get("/courses", response_model=list[CourseRead])
def list_courses(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    courses = session.exec(select(Course).where(Course.owner_id == current_user.id)).all()
    return [_serialize_course(course) for course in courses]


@router.post("/quizzes/submit", response_model=QuizSubmitResponse)
def submit_quiz(
    payload: QuizSubmit,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    course_exists = session.exec(
        select(Course).where(Course.id == payload.course_id, Course.owner_id == current_user.id)
    ).first()
    if not course_exists:
        raise HTTPException(status_code=404, detail="Course not found")

    signals = {action.strip().lower() for action in payload.suspicious_actions}
    flagged = any(signal in PROCTORING_SIGNALS for signal in signals)
    adjusted_score = max(payload.score - 10, 0) if flagged else payload.score

    attempt = QuizAttempt(
        user_id=current_user.id,
        course_id=payload.course_id,
        score=adjusted_score,
        flagged_cheating=flagged,
        reason=", ".join(sorted(signals)),
    )
    session.add(attempt)
    session.commit()
    return QuizSubmitResponse(
        score=adjusted_score,
        flagged_cheating=flagged,
        message="Quiz submitted with proctoring validation",
    )


@router.get("/suggestions", response_model=list[Suggestion])
def get_dynamic_suggestions(current_user: User = Depends(get_current_user)):
    interests = _interests_to_list(current_user.interests)
    base = interests or [current_user.target_track or "general"]
    return [
        Suggestion(
            title=f"Weekly {interest.title()} Practice Sprint",
            reason=f"Aligned to your interest in {interest}",
            type="practice",
        )
        for interest in base
    ] + [
        Suggestion(
            title="Interview Drill: Top Startups",
            reason="Behavioral + technical interview simulation",
            type="interview",
        )
    ]
