from django.urls import path

from . import views

urlpatterns = [
    path("", views.course_list_view, name="course-list"),
    path("my-courses/", views.my_courses_view, name="my-courses"),
    path("create/", views.create_course_view, name="create-course"),
    path("<slug:slug>/", views.course_detail_view, name="course-detail"),
    path("<slug:slug>/enroll/", views.enroll_view, name="enroll-course"),
    path("<slug:slug>/lesson/add/", views.add_lesson_view, name="add-lesson"),
    path("<slug:slug>/lesson/<int:lesson_id>/", views.lesson_detail_view, name="lesson-detail"),
    path("quiz/<int:quiz_id>/", views.quiz_attempt_view, name="quiz-attempt"),
]
