from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.user import UserPublic


class CategoryBase(BaseModel):
    name: str
    slug: str


class CategoryCreate(CategoryBase):
    pass


class CategoryOut(CategoryBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class CourseBase(BaseModel):
    title: str = Field(..., max_length=200)
    description: str
    category_id: int | None = None
    level: str = "beginner"
    is_published: bool = False


class CourseCreate(CourseBase):
    slug: str | None = None


class CourseUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    category_id: int | None = None
    level: str | None = None
    is_published: bool | None = None
    thumbnail_url: str | None = None


class CourseOut(CourseBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    thumbnail_url: str | None = None
    instructor: UserPublic
    category: CategoryOut | None = None
    average_rating: float | None = None
    enrollment_count: int = 0
    created_at: datetime
    updated_at: datetime


class LessonBase(BaseModel):
    title: str
    content: str | None = None
    video_url: str | None = None
    order: int = 0
    duration_minutes: int | None = None


class LessonCreate(LessonBase):
    course_id: int


class LessonOut(LessonBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    course_id: int
    created_at: datetime


class EnrollmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    course: CourseOut
    progress_percent: float
    is_completed: bool
    enrolled_at: datetime


class ReviewCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: str | None = None


class ReviewOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user: UserPublic
    rating: int
    comment: str | None = None
    created_at: datetime