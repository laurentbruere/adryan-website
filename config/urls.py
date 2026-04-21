from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.welcome, name="welcome"),
    path("planning/", views.planning, name="planning"),
    path("timetable/", views.timetable, name="timetable"),
    path("feedback/", views.feedback, name="feedback"),
]
