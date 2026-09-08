from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Notification


@login_required
def notifications_view(request):
    notifications = request.user.notifications.all()
    notifications.filter(is_read=False).update(is_read=True)
    return render(request, "notifications/notifications.html", {"notifications": notifications})


@login_required
def mark_read_view(request, pk):
    notification = get_object_or_404(Notification, id=pk, recipient=request.user)
    notification.is_read = True
    notification.save(update_fields=["is_read"])
    if notification.link:
        return redirect(notification.link)
    return redirect("notifications")
