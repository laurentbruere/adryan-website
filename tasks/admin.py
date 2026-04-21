from django.contrib import admin

from .models import Feedback, TimetableSlot, TodoItem


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("created_at", "message_preview", "name", "email")
    list_filter = ("created_at",)
    readonly_fields = ("created_at",)

    @admin.display(description="Message")
    def message_preview(self, obj):
        text = (obj.message or "").replace("\n", " ")
        return (text[:80] + "…") if len(text) > 80 else text


@admin.register(TimetableSlot)
class TimetableSlotAdmin(admin.ModelAdmin):
    list_display = ("weekday", "hour", "label", "importance")
    list_filter = ("weekday", "importance")


@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    list_display = ("title", "is_done", "created_at")
    list_filter = ("is_done",)
