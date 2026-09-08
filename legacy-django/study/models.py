from django.conf import settings
from django.db import models
from django.urls import reverse

User = settings.AUTH_USER_MODEL


class Topic(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="rooms")
    participants = models.ManyToManyField(User, related_name="joined_rooms", blank=True)
    likes = models.ManyToManyField(User, related_name="liked_rooms", blank=True)
    is_pinned = models.BooleanField(default=False)
    scheduled_for = models.DateTimeField(null=True, blank=True)
    max_participants = models.PositiveIntegerField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_pinned", "-updated", "-created"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("room", kwargs={"pk": self.pk})

    @property
    def is_full(self):
        if self.max_participants is None:
            return False
        return self.participants.count() >= self.max_participants


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookmarked_by")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "room")


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies")
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return self.body[:50]
