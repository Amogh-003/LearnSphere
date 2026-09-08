from rest_framework import serializers

from study.models import Room, Topic, Message, Tag
from courses.models import Course, Lesson, Category, Review
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "avatar", "headline", "points"]


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ["id", "name"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ["id", "user", "room", "parent", "body", "created", "updated"]


class RoomSerializer(serializers.ModelSerializer):
    host = UserSerializer(read_only=True)
    topic = TopicSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    participants_count = serializers.IntegerField(source="participants.count", read_only=True)
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)

    class Meta:
        model = Room
        fields = [
            "id", "host", "topic", "name", "description", "tags",
            "participants_count", "likes_count", "is_pinned",
            "scheduled_for", "max_participants", "created", "updated",
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "title", "content", "video_url", "order", "duration_minutes", "is_preview"]


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ["id", "user", "rating", "comment", "created"]


class CourseSerializer(serializers.ModelSerializer):
    instructor = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    enrolled_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = [
            "id", "instructor", "category", "title", "slug", "description",
            "thumbnail", "level", "price", "is_published", "lessons",
            "average_rating", "enrolled_count", "created", "updated",
        ]
