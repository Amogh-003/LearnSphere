from django.urls import path

from . import views

urlpatterns = [
    path("", views.notifications_view, name="notifications"),
    path("<int:pk>/read/", views.mark_read_view, name="mark-notification-read"),
]
