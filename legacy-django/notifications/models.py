from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

NOTIFICATION_TYPES = [
    ("follow", "New Follower"),
    ("like", "Room Liked"),
    ("reply", "Message Reply"),
    ("enrollment", "New Enrollment"),
    ("system", "System"),
]


class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+", null=True)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    text = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True)
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"{self.notification_type} -> {self.recipient}"
