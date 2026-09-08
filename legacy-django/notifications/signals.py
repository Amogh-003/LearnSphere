from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from users.models import Follow
from study.models import Room, Message
from courses.models import Enrollment
from .models import Notification


@receiver(post_save, sender=Follow)
def notify_new_follower(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.following,
            actor=instance.follower,
            notification_type="follow",
            text=f"{instance.follower.username} started following you.",
            link=f"/users/profile/{instance.follower.id}/",
        )


@receiver(post_save, sender=Message)
def notify_reply(sender, instance, created, **kwargs):
    if created and instance.parent and instance.parent.user != instance.user:
        Notification.objects.create(
            recipient=instance.parent.user,
            actor=instance.user,
            notification_type="reply",
            text=f"{instance.user.username} replied to your message.",
            link=f"/room/{instance.room_id}/",
        )


@receiver(post_save, sender=Enrollment)
def notify_enrollment(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.course.instructor,
            actor=instance.student,
            notification_type="enrollment",
            text=f"{instance.student.username} enrolled in {instance.course.title}.",
            link=f"/courses/{instance.course.slug}/",
        )


@receiver(m2m_changed, sender=Room.likes.through)
def notify_like(sender, instance, action, pk_set, **kwargs):
    if action == "post_add" and pk_set:
        from users.models import User

        for user_id in pk_set:
            actor = User.objects.get(id=user_id)
            if actor != instance.host:
                Notification.objects.create(
                    recipient=instance.host,
                    actor=actor,
                    notification_type="like",
                    text=f"{actor.username} liked your room '{instance.name}'.",
                    link=f"/room/{instance.id}/",
                )
