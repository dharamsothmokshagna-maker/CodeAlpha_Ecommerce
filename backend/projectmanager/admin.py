from django.contrib import admin
from .models import Project, Task, Comment


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "created_at")
    search_fields = ("name", "description")
    list_filter = ("created_at",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "project",
        "assigned_to",
        "status",
        "created_at",
    )
    search_fields = ("title", "description")
    list_filter = ("status", "created_at")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "task",
        "user",
        "created_at",
    )
    search_fields = ("content",)
    list_filter = ("created_at",)