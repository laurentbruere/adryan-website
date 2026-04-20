from django.urls import path

from . import views

urlpatterns = [
    path("", views.welcome, name="welcome"),
    path("planning/", views.planning, name="planning"),
]
