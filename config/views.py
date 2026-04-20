from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from tasks.models import TodoItem


def welcome(request):
    return render(request, "home.html")


@require_http_methods(["GET", "POST"])
def planning(request):
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "add":
            title = (request.POST.get("title") or "").strip()
            if title:
                TodoItem.objects.create(title=title)
        elif action == "toggle":
            todo = _get_todo(request.POST.get("id"))
            if todo:
                todo.is_done = not todo.is_done
                todo.save()
        elif action == "delete":
            todo = _get_todo(request.POST.get("id"))
            if todo:
                todo.delete()
        return redirect("planning")

    todos = list(TodoItem.objects.all())
    return render(request, "planning.html", {"todos": todos})


def _get_todo(pk_raw):
    if not pk_raw or not str(pk_raw).isdigit():
        return None
    try:
        return TodoItem.objects.get(pk=int(pk_raw))
    except TodoItem.DoesNotExist:
        return None
