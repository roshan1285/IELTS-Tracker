from django.db import models

# Create your models here.
from django.conf import settings

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    THEME_CHOICES = [
        (0, "Light"),
        (1, "Dark"),
    ]

    full_name = models.CharField(max_length=150, blank=True)

    # Current scores
    CL = models.DecimalField("Current Listening", max_digits=3, decimal_places=1, null=True, blank=True)
    CR = models.DecimalField("Current Reading", max_digits=3, decimal_places=1, null=True, blank=True)
    CW = models.DecimalField("Current Writing", max_digits=3, decimal_places=1, null=True, blank=True)
    CS = models.DecimalField("Current Speaking", max_digits=3, decimal_places=1, null=True, blank=True)
    CO = models.DecimalField("Current Overall", max_digits=3, decimal_places=1, null=True, blank=True)

    # Targeted scores
    TL = models.DecimalField("Targeted Listening", max_digits=3, decimal_places=1, null=True, blank=True)
    TR = models.DecimalField("Targeted Reading", max_digits=3, decimal_places=1, null=True, blank=True)
    TW = models.DecimalField("Targeted Writing", max_digits=3, decimal_places=1, null=True, blank=True)
    TS = models.DecimalField("Targeted Speaking", max_digits=3, decimal_places=1, null=True, blank=True)
    TO = models.DecimalField("Targeted Overall", max_digits=3, decimal_places=1, null=True, blank=True)

    exam_date = models.DateField(null=True, blank=True)
    preferred_theme = models.PositiveSmallIntegerField(choices=THEME_CHOICES, default=0)

    def __str__(self):
        return self.full_name or self.username
    
class WritingTest(models.Model):
    TASK_CHOICES = [
        ("task1", "Task 1"),
        ("task2", "Task 2"),
        ("full", "Full test (Task 1 + Task 2)"),
    ]
    STATUS_CHOICES = [
        ("in_progress", "In progress"),
        ("completed", "Completed"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="writing_tests",
    )
    task_type = models.CharField(max_length=10, choices=TASK_CHOICES, default="task1")
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="in_progress")

    task1_prompt = models.TextField(blank=True)
    task1_image = models.ImageField(upload_to="writing_prompts/", blank=True, null=True)
    task1_answer = models.TextField(blank=True)
    task1_score = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)

    task2_prompt = models.TextField(blank=True)
    task2_answer = models.TextField(blank=True)
    task2_score = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)

    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-started_at"]

    @property
    def overall_score(self):
        scores = [s for s in [self.task1_score, self.task2_score] if s is not None]
        if not scores:
            return None
        return round(sum(scores) / len(scores), 1)

    def __str__(self):
        return f"{self.user} — {self.get_task_type_display()} ({self.started_at:%d %b %Y})"