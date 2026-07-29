from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Project, Task , Comment


@login_required
def project_list(request):
    projects = Project.objects.all().order_by("-created_at")

    return render(
        request,
        "projectmanager/project_list.html",
        {"projects": projects}
    )


@login_required
def create_project(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")

        Project.objects.create(
            name=name,
            description=description,
            owner=request.user
        )

        return redirect("projectmanager:project_list")

    return render(
        request,
        "projectmanager/create_project.html"
    )


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    return render(
        request,
        "projectmanager/project_detail.html",
        {"project": project}
    )
@login_required
def create_task(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        assigned_to_id = request.POST.get("assigned_to")
        status = request.POST.get("status")

        assigned_user = None

        if assigned_to_id:
            assigned_user = get_object_or_404(
                User,
                id=assigned_to_id
            )

        Task.objects.create(
            project=project,
            title=title,
            description=description,
            assigned_to=assigned_user,
            status=status
        )

        return redirect(
            "projectmanager:project_detail",
            project_id=project.id
        )

    return render(
        request,
        "projectmanager/create_task.html",
        {
            "project": project,
            "users": User.objects.all()
        }
    )
@login_required
def update_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        status = request.POST.get("status")

        if status in ["todo", "progress", "completed"]:
            task.status = status
            task.save()

    return redirect(
        "projectmanager:project_detail",
        project_id=task.project.id
    )
@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        content = request.POST.get("content")

        if content:
            Comment.objects.create(
                task=task,
                user=request.user,
                content=content
            )

        return redirect(
            "projectmanager:task_detail",
            task_id=task.id
        )

    return render(
        request,
        "projectmanager/task_detail.html",
        {
            "task": task,
            "comments": task.comments.all().order_by("-created_at")
        }
    )