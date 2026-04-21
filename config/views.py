from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from tasks.models import Feedback, TimetableSlot, TodoItem


def welcome(request):
    return render(request, "home.html")


@require_http_methods(["GET", "POST"])
def feedback(request):
    if request.method == "POST":
        message_text = (request.POST.get("message") or "").strip()
        name = (request.POST.get("name") or "").strip()[:120]
        email = (request.POST.get("email") or "").strip()[:254]
        if message_text:
            Feedback.objects.create(message=message_text, name=name, email=email)
            messages.success(request, "Thank you—your feedback has been received.")
        else:
            messages.error(request, "Please enter a message before sending.")
        return redirect("feedback")

    return render(request, "feedback.html")


_WEEKDAYS = (
    ("mon", "Mon"),
    ("tue", "Tue"),
    ("wed", "Wed"),
    ("thu", "Thu"),
    ("fri", "Fri"),
    ("sat", "Sat"),
    ("sun", "Sun"),
)
_WEEKDAY_KEYS = frozenset(k for k, _ in _WEEKDAYS)
_IMPORTANCE_VALUES = frozenset(
    {TimetableSlot.IMPORTANCE_LOW, TimetableSlot.IMPORTANCE_MEDIUM, TimetableSlot.IMPORTANCE_HIGH}
)


def _parse_hour_param(raw, default):
    if raw is None or raw == "":
        return default
    try:
        v = int(raw)
    except (TypeError, ValueError):
        return default
    return max(0, min(23, v))


def _timetable_redirect(from_h, to_h):
    return redirect(f"{reverse('timetable')}?from={from_h}&to={to_h}")


def _parse_weekday(raw):
    if not raw or raw not in _WEEKDAY_KEYS:
        return None
    return raw


def _parse_slot_hour(raw):
    if raw is None or raw == "" or not str(raw).isdigit():
        return None
    h = int(raw)
    if h < 0 or h > 23:
        return None
    return h


def _timetable_rows(hours, slot_map):
    rows = []
    for hour in hours:
        cells = []
        for day_key, _day_label in _WEEKDAYS:
            slot = slot_map.get((day_key, hour))
            label = slot.label if slot else ""
            importance = (
                slot.importance
                if slot
                else TimetableSlot.IMPORTANCE_MEDIUM
            )
            cells.append(
                {
                    "day_key": day_key,
                    "hour": hour,
                    "label": label,
                    "importance": importance,
                    "display": label if label else "—",
                }
            )
        rows.append({"hour": hour, "cells": cells})
    return rows


@require_http_methods(["GET", "POST"])
def timetable(request):
    default_from, default_to = 0, 23

    if request.method == "POST":
        from_h = _parse_hour_param(request.POST.get("range_from"), default_from)
        to_h = _parse_hour_param(request.POST.get("range_to"), default_to)
        if from_h > to_h:
            from_h, to_h = default_from, default_to

        weekday = _parse_weekday(request.POST.get("weekday"))
        hour = _parse_slot_hour(request.POST.get("hour"))
        if weekday is not None and hour is not None:
            action = (request.POST.get("action") or "").strip()
            if action == "clear":
                TimetableSlot.objects.filter(weekday=weekday, hour=hour).delete()
            else:
                label = (request.POST.get("label") or "").strip()
                importance = request.POST.get("importance") or TimetableSlot.IMPORTANCE_MEDIUM
                if importance not in _IMPORTANCE_VALUES:
                    importance = TimetableSlot.IMPORTANCE_MEDIUM
                if not label:
                    TimetableSlot.objects.filter(weekday=weekday, hour=hour).delete()
                else:
                    TimetableSlot.objects.update_or_create(
                        weekday=weekday,
                        hour=hour,
                        defaults={"label": label, "importance": importance},
                    )

        return _timetable_redirect(from_h, to_h)

    from_h = _parse_hour_param(request.GET.get("from"), default_from)
    to_h = _parse_hour_param(request.GET.get("to"), default_to)
    if from_h > to_h:
        from_h, to_h = default_from, default_to

    hours = list(range(from_h, to_h + 1))
    weekdays = [{"key": k, "label": lab} for k, lab in _WEEKDAYS]

    slot_map = {
        (s.weekday, s.hour): s
        for s in TimetableSlot.objects.filter(
            hour__gte=from_h,
            hour__lte=to_h,
        )
    }
    rows = _timetable_rows(hours, slot_map)

    return render(
        request,
        "timetable.html",
        {
            "hours": hours,
            "weekdays": weekdays,
            "rows": rows,
            "range_from": from_h,
            "range_to": to_h,
            "hour_choices": list(range(24)),
        },
    )


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
