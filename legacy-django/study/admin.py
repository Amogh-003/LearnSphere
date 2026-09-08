from django.contrib import admin

from .models import Topic, Room, Message, Tag, Bookmark

admin.site.register(Topic)
admin.site.register(Tag)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Bookmark)
