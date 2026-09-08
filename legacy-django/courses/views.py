from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import CourseForm, LessonForm, ReviewForm
from .models import Course, Category, Lesson, Enrollment, LessonProgress, Quiz, QuizAttempt, Review


def course_list_view(request):
    q = request.GET.get("q", "")
    category_slug = request.GET.get("category", "")
    level = request.GET.get("level", "")

    courses = Course.objects.filter(is_published=True).filter(
        Q(title__icontains=q) | Q(description__icontains=q)
    )
    if category_slug:
        courses = courses.filter(category__slug=category_slug)
    if level:
        courses = courses.filter(level=level)

    paginator = Paginator(courses, 9)
    page_obj = paginator.get_page(request.GET.get("page"))
    categories = Category.objects.all()

    context = {
        "courses": page_obj,
        "categories": categories,
        "q": q,
        "level": level,
    }
    return render(request, "courses/course_list.html", context)


def course_detail_view(request, slug):
    course = get_object_or_404(Course, slug=slug)
    lessons = course.lessons.all()
    is_enrolled = (
        request.user.is_authenticated
        and Enrollment.objects.filter(student=request.user, course=course).exists()
    )
    reviews = course.reviews.select_related("user")
    review_form = ReviewForm()

    if request.method == "POST" and request.user.is_authenticated:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review, _created = Review.objects.update_or_create(
                course=course,
                user=request.user,
                defaults=review_form.cleaned_data,
            )
            return redirect("course-detail", slug=slug)

    context = {
        "course": course,
        "lessons": lessons,
        "is_enrolled": is_enrolled,
        "reviews": reviews,
        "review_form": review_form,
    }
    return render(request, "courses/course_detail.html", context)


@login_required
def enroll_view(request, slug):
    course = get_object_or_404(Course, slug=slug)
    Enrollment.objects.get_or_create(student=request.user, course=course)
    messages.success(request, f"Enrolled in {course.title}.")
    return redirect("course-detail", slug=slug)


@login_required
def lesson_detail_view(request, slug, lesson_id):
    course = get_object_or_404(Course, slug=slug)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    enrollment = Enrollment.objects.filter(student=request.user, course=course).first()

    if not enrollment and not lesson.is_preview:
        messages.error(request, "Enroll in this course to access this lesson.")
        return redirect("course-detail", slug=slug)

    quiz = getattr(lesson, "quiz", None)

    if request.method == "POST" and enrollment:
        progress, _created = LessonProgress.objects.get_or_create(enrollment=enrollment, lesson=lesson)
        progress.is_completed = True
        progress.completed_at = timezone.now()
        progress.save()
        if enrollment.progress_percent == 100:
            enrollment.completed = True
            enrollment.completed_at = timezone.now()
            enrollment.save()
            request.user.add_points(20)
        return redirect("lesson-detail", slug=slug, lesson_id=lesson.id)

    context = {
        "course": course,
        "lesson": lesson,
        "enrollment": enrollment,
        "quiz": quiz,
    }
    return render(request, "courses/lesson_detail.html", context)


@login_required
def quiz_attempt_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.prefetch_related("choices")

    if request.method == "POST":
        total = questions.count()
        correct = 0
        for question in questions:
            selected_id = request.POST.get(f"question_{question.id}")
            if selected_id and question.choices.filter(id=selected_id, is_correct=True).exists():
                correct += 1
        score = round((correct / total) * 100) if total else 0
        passed = score >= quiz.pass_score
        QuizAttempt.objects.create(user=request.user, quiz=quiz, score=score, passed=passed)
        if passed:
            request.user.add_points(10)
        return render(request, "quiz/quiz_result.html", {"quiz": quiz, "score": score, "passed": passed})

    return render(request, "quiz/quiz_detail.html", {"quiz": quiz, "questions": questions})


@login_required
def my_courses_view(request):
    enrollments = Enrollment.objects.filter(student=request.user).select_related("course")
    teaching = Course.objects.filter(instructor=request.user)
    return render(request, "courses/my_courses.html", {"enrollments": enrollments, "teaching": teaching})


@login_required
def create_course_view(request):
    form = CourseForm()
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            return redirect("course-detail", slug=course.slug)
    return render(request, "courses/course_form.html", {"form": form})


@login_required
def add_lesson_view(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if request.user != course.instructor:
        return HttpResponseForbidden("You are not the instructor of this course.")

    form = LessonForm()
    if request.method == "POST":
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            return redirect("course-detail", slug=slug)
    return render(request, "courses/lesson_form.html", {"form": form, "course": course})
