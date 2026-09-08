from django import forms

from .models import Room, Message


class RoomForm(forms.ModelForm):
    tags_input = forms.CharField(
        required=False, help_text="Comma separated tags, e.g. python, django, api"
    )

    class Meta:
        model = Room
        fields = [
            "topic",
            "name",
            "description",
            "scheduled_for",
            "max_participants",
        ]
        widgets = {
            "scheduled_for": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["body"]
        widgets = {"body": forms.Textarea(attrs={"rows": 2, "placeholder": "Write a message..."})}
