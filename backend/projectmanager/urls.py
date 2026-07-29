from django.urls import path
from . import views

app_name = "projectmanager"

urlpatterns = [
    path("", views.project_list, name="project_list"),

    path(
        "create/",
        views.create_project,
        name="create_project"
    ),

    path(
        "<int:project_id>/",
        views.project_detail,
        name="project_detail"
    ),

    path(
        "<int:project_id>/tasks/create/",
        views.create_task,
        name="create_task"
    ),

    path(
        "tasks/<int:task_id>/status/",
        views.update_task_status,
        name="update_task_status"
    ),
    
    path(
    "tasks/<int:task_id>/",
    views.task_detail,
    name="task_detail"
),
]