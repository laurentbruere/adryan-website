from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class TimetableSlot(models.Model):
    WEEKDAY_CHOICES = (
        ("mon", "Monday"),
        ("tue", "Tuesday"),
        ("wed", "Wednesday"),
        ("thu", "Thursday"),
        ("fri", "Friday"),
        ("sat", "Saturday"),
        ("sun", "Sunday"),
    )
    IMPORTANCE_LOW = "low"
    IMPORTANCE_MEDIUM = "medium"
    IMPORTANCE_HIGH = "high"
    IMPORTANCE_CHOICES = (
        (IMPORTANCE_LOW, "Low"),
        (IMPORTANCE_MEDIUM, "Medium"),
        (IMPORTANCE_HIGH, "High"),
    )

    weekday = models.CharField(max_length=3, choices=WEEKDAY_CHOICES)
    hour = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(23)])
    label = models.CharField(max_length=200, blank=True)
    importance = models.CharField(
        max_length=10,
        choices=IMPORTANCE_CHOICES,
        default=IMPORTANCE_MEDIUM,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["weekday", "hour"],
                name="uniq_timetable_weekday_hour",
            ),
        ]

    def __str__(self):
        return f"{self.get_weekday_display()} {self.hour:02d}:00 — {self.label or '(empty)'}"


class Feedback(models.Model):
    message = models.TextField()
    name = models.CharField(max_length=120, blank=True)
    email = models.CharField(max_length=254, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (self.message[:60] + "…") if len(self.message) > 60 else self.message


class TodoItem(models.Model):
    title = models.CharField(max_length=200)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
