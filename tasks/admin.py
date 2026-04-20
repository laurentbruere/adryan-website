from django.contrib import admin

from .models import TodoItem


@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    list_display = ("title", "is_done", "created_at")
    list_filter = ("is_done",)
