from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RoomForm, MessageForm
from .models import Room, Topic, Message, Tag, Bookmark


def home_view(request):
    q = request.GET.get("q", "")
    tag_slug = request.GET.get("tag", "")

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q)
        | Q(name__icontains=q)
        | Q(description__icontains=q)
    )
    if tag_slug:
        rooms = rooms.filter(tags__name__iexact=tag_slug)

    topics = Topic.objects.annotate(room_count=Count("room")).order_by("-room_count")[:6]
    tags = Tag.objects.all()

    paginator = Paginator(rooms.distinct(), 8)
    page_obj = paginator.get_page(request.GET.get("page"))

    room_count = Room.objects.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q)
    ).order_by("-created")[:5]

    context = {
        "rooms": page_obj,
        "topics": topics,
        "tags": tags,
        "room_count": room_count,
        "room_messages": room_messages,
        "q": q,
    }
    return render(request, "home.html", context)


def room_view(request, pk):
    room = get_object_or_404(Room, id=pk)
    room_messages = room.message_set.filter(parent__isnull=True)
    participants = room.participants.all()

    if request.method == "POST" and request.user.is_authenticated:
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.room = room
            parent_id = request.POST.get("parent_id")
            if parent_id:
                message.parent_id = parent_id
            message.save()
            room.participants.add(request.user)
            request.user.add_points(2)
        return redirect("room", pk=room.id)

    context = {
        "room": room,
        "room_messages": room_messages,
        "participants": participants,
        "form": MessageForm(),
    }
    return render(request, "room.html", context)


def topics_view(request):
    q = request.GET.get("q", "")
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, "topics.html", {"topics": topics})


def activity_view(request):
    room_messages = Message.objects.all()[:20]
    return render(request, "activity.html", {"room_messages": room_messages})


@login_required
def create_room_view(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        form = RoomForm(request.POST)
        topic_name = request.POST.get("topic")
        topic, _created = Topic.objects.get_or_create(name=topic_name)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.topic = topic
            room.save()
            _sync_tags(room, form.cleaned_data.get("tags_input", ""))
            room.participants.add(request.user)
            request.user.add_points(5)
            messages.success(request, "Room created successfully.")
            return redirect("room", pk=room.id)
    return render(request, "room_form.html", {"form": form, "topics": topics})


@login_required
def update_room_view(request, pk):
    room = get_object_or_404(Room, id=pk)
    if request.user != room.host:
        return HttpResponseForbidden("You are not allowed to edit this room.")

    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        topic_name = request.POST.get("topic")
        topic, _created = Topic.objects.get_or_create(name=topic_name)
        if form.is_valid():
            room = form.save(commit=False)
            room.topic = topic
            room.save()
            _sync_tags(room, form.cleaned_data.get("tags_input", ""))
            return redirect("room", pk=room.id)

    return render(request, "room_form.html", {"form": form, "topics": topics, "room": room})


@login_required
def delete_room_view(request, pk):
    room = get_object_or_404(Room, id=pk)
    if request.user != room.host:
        return HttpResponseForbidden("You are not allowed to delete this room.")
    if request.method == "POST":
        room.delete()
        return redirect("home")
    return render(request, "delete.html", {"obj": room})


@login_required
def delete_message_view(request, pk):
    message = get_object_or_404(Message, id=pk)
    if request.user != message.user:
        return HttpResponseForbidden("You are not allowed to delete this message.")
    if request.method == "POST":
        room_id = message.room.id
        message.delete()
        return redirect("room", pk=room_id)
    return render(request, "delete.html", {"obj": message})


@login_required
def toggle_like_view(request, pk):
    room = get_object_or_404(Room, id=pk)
    if request.user in room.likes.all():
        room.likes.remove(request.user)
    else:
        room.likes.add(request.user)
        room.host.add_points(1)
    return redirect("room", pk=pk)


@login_required
def toggle_bookmark_view(request, pk):
    room = get_object_or_404(Room, id=pk)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, room=room)
    if not created:
        bookmark.delete()
    return redirect("room", pk=pk)


@login_required
def my_bookmarks_view(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related("room")
    return render(request, "bookmarks.html", {"bookmarks": bookmarks})


def _sync_tags(room, tags_input):
    room.tags.clear()
    for raw_tag in tags_input.split(","):
        name = raw_tag.strip().lower()
        if name:
            tag, _created = Tag.objects.get_or_create(name=name)
            room.tags.add(tag)
