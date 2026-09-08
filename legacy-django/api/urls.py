from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from . import views

router = DefaultRouter()
router.register("rooms", views.RoomViewSet)
router.register("topics", views.TopicViewSet)
router.register("tags", views.TagViewSet)
router.register("messages", views.MessageViewSet)
router.register("courses", views.CourseViewSet)
router.register("lessons", views.LessonViewSet)
router.register("categories", views.CategoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("token-auth/", obtain_auth_token, name="api-token-auth"),
]
