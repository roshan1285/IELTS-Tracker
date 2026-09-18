from django.db import models

# Create your models here.
from django.conf import settings

from django.contrib.auth.models import AbstractUser
from django.db import models

BAND_SCORE_CHOICES = [
    ( 9.0, "9.0"),
    ( 8.5, "8.5"),
    ( 8.0, "8.0"),
    ( 7.5, "7.5"),
    ( 7.0, "7.0"),
    ( 6.5, "6.5"),
    ( 6.0, "6.0"),
    ( 5.5, "5.5"),
    ( 5.0, "5.0"),
]

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
    task1_score = models.DecimalField(max_digits=3, decimal_places=1, default=5.5, choices=BAND_SCORE_CHOICES,null=True, blank=True)

    task2_prompt = models.TextField(blank=True)
    task2_answer = models.TextField(blank=True)
    task2_score = models.DecimalField(max_digits=3, decimal_places=1, default=5.5, choices=BAND_SCORE_CHOICES, null=True, blank=True)

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

class ListeningTest(models.Model):

    LISTENING_BAND_SCORE_CHOICES = [
        ( 9.0, "9.0 [39-40]"),
        ( 8.5, "8.5 [37-38]"),
        ( 8.0, "8.0 [35-36]"),
        ( 7.5, "7.5 [32-34]"),
        ( 7.0, "7.0 [30-31]"),
        ( 6.5, "6.5 [26-29]"),
        ( 6.0, "6.0 [23-25]"),
        ( 5.5, "5.5 [18-22]"),
        ( 5.0, "5.0 [16-17]"),
        ( 4.5, "4.5 [13-15]"),
        ( 4.0, "4.0 [11-12]"),
        ( 3.5, "3.5 [8-10]"),
        ( 3.0, "3.0 [6-7]"),
        ( 2.5, "2.5 [4-5]"),
        ( 2.0, "2.0 [3]"),
        ( 1.5, "1.5 [2]"),
        ( 1.0, "1.0 [1]"),
        ( 0.0, "0.0 [0]"),
    ]
        
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="listening_tests",
    )
    answers = models.JSONField(default=list, blank=True)  # 40 optional notes
    score = models.PositiveSmallIntegerField(null=True, blank=True)  # out of 40
    taken_at = models.DateTimeField(auto_now_add=True)
    band = models.DecimalField(max_digits=3, decimal_places=1, choices=LISTENING_BAND_SCORE_CHOICES, default=5.5)

    class Meta:
        ordering = ["-taken_at"]

    def __str__(self):
        return f"{self.user} — Listening ({self.taken_at:%d %b %Y})"

    def calculate_listening_band_score(self):

        if self.score is None:
            return None

        if self.score >= 39: return 9.0
        if self.score >= 38: return 8.5
        if self.score >= 36: return 8.0
        if self.score >= 34: return 7.5
        if self.score >= 31: return 7.0
        if self.score >= 29: return 6.5
        if self.score >= 25: return 6.0
        if self.score >= 22: return 5.5
        if self.score >= 17: return 5.0
        if self.score >= 15: return 4.5
        if self.score >= 12: return 4.0
        if self.score >= 10: return 3.5
        if self.score >= 7: return 3.0
        if self.score >= 5: return 2.5
        if self.score == 3: return 2.0
        if self.score == 2: return 1.5
        if self.score == 1: return 1.0
        return 0.0

    def save(self, *args, **kwargs):

        if self.score is not None:
            self.band = self.calculate_listening_band_score()

        super().save(*args, **kwargs)
        
class ReadingTest(models.Model):

    READING_BAND_SCORE_CHOICES = [
            ( 9.0, "9.0 [39-40]"),
            ( 8.5, "8.5 [37-38]"),
            ( 8.0, "8.0 [35-36]"),
            ( 7.5, "7.5 [33-34]"),
            ( 7.0, "7.0 [30-32]"),
            ( 6.5, "6.5 [27-29]"),
            ( 6.0, "6.0 [23-26]"),
            ( 5.5, "5.5 [19-22]"),
            ( 5.0, "5.0 [15-18]"),
            ( 4.5, "4.5 [13-14]"),
            ( 4.0, "4.0 [10-12]"),
            ( 3.5, "3.5 [8-9]"),
            ( 3.0, "3.0 [6-7]"),
            ( 2.5, "2.5 [4-5]"),
            ( 2.0, "2.0 [3]"),
            ( 1.5, "1.5 [2]"),
            ( 1.0, "1.0 [1]"),
            ( 0.0, "0.0 [0]"),
        ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reading_tests",
    )
    answers = models.JSONField(default=list, blank=True)  # 40 optional notes
    score = models.PositiveSmallIntegerField(null=True, blank=True)  # out of 40
    taken_at = models.DateTimeField(auto_now_add=True)
    band = models.DecimalField(max_digits=3, decimal_places=1, choices=READING_BAND_SCORE_CHOICES, default=5.5)


    class Meta:
        ordering = ["-taken_at"]

    def __str__(self):
        return f"{self.user} — Reading ({self.taken_at:%d %b %Y})"

    def calculate_reading_band_score(self):

        if self.score is None:
            return None

        if self.score >= 39: return 9.0
        if self.score >= 38: return 8.5
        if self.score >= 36: return 8.0
        if self.score >= 34: return 7.5
        if self.score >= 32: return 7.0
        if self.score >= 29: return 6.5
        if self.score >= 26: return 6.0
        if self.score >= 22: return 5.5
        if self.score >= 18: return 5.0
        if self.score >= 14: return 4.5
        if self.score >= 12: return 4.0
        if self.score >= 9: return 3.5
        if self.score >= 7: return 3.0
        if self.score >= 5: return 2.5
        if self.score == 3: return 2.0
        if self.score == 2: return 1.5
        if self.score == 1: return 1.0
        return 0.0

    def save(self, *args, **kwargs):

        if self.score is not None:
            self.band = self.calculate_reading_band_score()

        super().save(*args, **kwargs)