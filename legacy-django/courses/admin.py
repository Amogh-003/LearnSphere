from django.contrib import admin

from .models import Category, Course, Lesson, Enrollment, LessonProgress, Quiz, Question, Choice, QuizAttempt, Review


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["title", "instructor", "level", "price", "is_published", "created"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [LessonInline]


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]


admin.site.register(Category)
admin.site.register(Lesson)
admin.site.register(Enrollment)
admin.site.register(LessonProgress)
admin.site.register(QuizAttempt)
admin.site.register(Review)
