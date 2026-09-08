from django import forms

from .models import Course, Lesson, Review


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["category", "title", "slug", "description", "thumbnail", "level", "price", "is_published"]


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ["title", "content", "video_url", "order", "duration_minutes", "is_preview"]


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {"rating": forms.NumberInput(attrs={"min": 1, "max": 5})}
