from django.urls import path

from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("room/<str:pk>/", views.room_view, name="room"),
    path("room-create/", views.create_room_view, name="create-room"),
    path("room-update/<str:pk>/", views.update_room_view, name="update-room"),
    path("room-delete/<str:pk>/", views.delete_room_view, name="delete-room"),
    path("message-delete/<str:pk>/", views.delete_message_view, name="delete-message"),
    path("room-like/<str:pk>/", views.toggle_like_view, name="toggle-like"),
    path("room-bookmark/<str:pk>/", views.toggle_bookmark_view, name="toggle-bookmark"),
    path("my-bookmarks/", views.my_bookmarks_view, name="my-bookmarks"),
    path("topics/", views.topics_view, name="topics"),
    path("activity/", views.activity_view, name="activity"),
]
