from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
import re

from app.core.database import get_db
from app.models.user import User
from app.models.course import Course, Category, Lesson, Enrollment, Review
from app.schemas.course import (
    CourseCreate,
    CourseUpdate,
    CourseOut,
    CategoryOut,
    LessonCreate,
    LessonOut,
    EnrollmentOut,
    ReviewCreate,
    ReviewOut,
)
from app.schemas.user import UserPublic
from app.api.deps import get_current_user

router = APIRouter(prefix="/courses", tags=["courses"])


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[-\s]+", "-", text)


def course_to_out(course: Course) -> CourseOut:
    avg = None
    if course.reviews:
        avg = sum(r.rating for r in course.reviews) / len(course.reviews)
    return CourseOut(
        id=course.id,
        title=course.title,
        slug=course.slug,
        description=course.description,
        category_id=course.category_id,
        level=course.level,
        is_published=course.is_published,
        thumbnail_url=course.thumbnail_url,
        instructor=UserPublic.model_validate(course.instructor),
        category=CategoryOut.model_validate(course.category) if course.category else None,
        average_rating=round(avg, 1) if avg is not None else None,
        enrollment_count=len(course.enrollments),
        created_at=course.created_at,
        updated_at=course.updated_at,
    )


@router.get("/", response_model=list[CourseOut])
async def list_courses(
    q: str | None = None,
    category_id: int | None = None,
    level: str | None = None,
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
):
    query = (
        select(Course)
        .where(Course.is_published == True)
        .options(
            selectinload(Course.instructor),
            selectinload(Course.category),
            selectinload(Course.reviews),
            selectinload(Course.enrollments),
        )
        .order_by(Course.created_at.desc())
    )
    if q:
        query = query.where(
            (Course.title.ilike(f"%{q}%")) | (Course.description.ilike(f"%{q}%"))
        )
    if category_id:
        query = query.where(Course.category_id == category_id)
    if level:
        query = query.where(Course.level == level)

    result = await db.execute(query.offset(skip).limit(limit))
    courses = result.scalars().all()
    return [course_to_out(c) for c in courses]


@router.post("/", response_model=CourseOut, status_code=status.HTTP_201_CREATED)
async def create_course(
    course_in: CourseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    slug = course_in.slug or slugify(course_in.title)
    # ensure unique
    base_slug = slug
    counter = 1
    while True:
        result = await db.execute(select(Course).where(Course.slug == slug))
        if not result.scalar_one_or_none():
            break
        slug = f"{base_slug}-{counter}"
        counter += 1

    course = Course(
        instructor_id=current_user.id,
        title=course_in.title,
        slug=slug,
        description=course_in.description,
        category_id=course_in.category_id,
        level=course_in.level,
        is_published=course_in.is_published,
    )
    db.add(course)
    await db.flush()

    result = await db.execute(
        select(Course)
        .where(Course.id == course.id)
        .options(
            selectinload(Course.instructor),
            selectinload(Course.category),
            selectinload(Course.reviews),
            selectinload(Course.enrollments),
        )
    )
    course = result.scalar_one()
    return course_to_out(course)


@router.get("/{course_id}", response_model=CourseOut)
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Course)
        .where(Course.id == course_id)
        .options(
            selectinload(Course.instructor),
            selectinload(Course.category),
            selectinload(Course.reviews),
            selectinload(Course.enrollments),
        )
    )
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course_to_out(course)


@router.post("/{course_id}/enroll", response_model=EnrollmentOut)
async def enroll_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    result = await db.execute(
        select(Enrollment).where(
            Enrollment.user_id == current_user.id, Enrollment.course_id == course_id
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Already enrolled")

    enrollment = Enrollment(user_id=current_user.id, course_id=course_id)
    db.add(enrollment)
    await db.flush()

    result = await db.execute(
        select(Enrollment)
        .where(Enrollment.id == enrollment.id)
        .options(
            selectinload(Enrollment.course).selectinload(Course.instructor),
            selectinload(Enrollment.course).selectinload(Course.category),
            selectinload(Enrollment.course).selectinload(Course.reviews),
            selectinload(Enrollment.course).selectinload(Course.enrollments),
        )
    )
    enrollment = result.scalar_one()
    return EnrollmentOut(
        id=enrollment.id,
        course=course_to_out(enrollment.course),
        progress_percent=enrollment.progress_percent,
        is_completed=enrollment.is_completed,
        enrolled_at=enrollment.enrolled_at,
    )


@router.get("/{course_id}/lessons", response_model=list[LessonOut])
async def list_lessons(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Lesson).where(Lesson.course_id == course_id).order_by(Lesson.order)
    )
    return result.scalars().all()


@router.post("/{course_id}/reviews", response_model=ReviewOut, status_code=status.HTTP_201_CREATED)
async def create_review(
    course_id: int,
    review_in: ReviewCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Course).where(Course.id == course_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Course not found")

    review = Review(
        user_id=current_user.id,
        course_id=course_id,
        rating=review_in.rating,
        comment=review_in.comment,
    )
    db.add(review)
    await db.flush()
    await db.refresh(review)

    result = await db.execute(
        select(Review).where(Review.id == review.id).options(selectinload(Review.user))
    )
    review = result.scalar_one()
    return review