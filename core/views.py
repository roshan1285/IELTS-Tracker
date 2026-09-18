from django.shortcuts import render
from datetime import date

# Create your views here.

MAX_BAND = 9.0

def days_to_exam():
    today = date.today()

    target_date = date(2026, 10, 19)

    time_difference = target_date - today

    remaining_days = time_difference.days

    return remaining_days
    # print(f"Remaining days: {remaining_days}")

def _with_pct(entries):
    """Attach current_pct / target_pct (0-100) for bar widths."""
    for e in entries:
        e["current_pct"] = round(e["current"] / MAX_BAND * 100, 1)
        e["target_pct"] = round(e["target"] / MAX_BAND * 100, 1)
    return entries


def home(request):
    # --- Static placeholder data. Replace with real queries once the
    # models exist, e.g. TestRecord.objects.filter(user=request.user)... ---

    modules = _with_pct([
        {"name": "Listening", "slug": "listening", "current": 8.0, "target": 8.5},
        {"name": "Reading", "slug": "reading", "current": 7.0, "target": 7.5},
        {"name": "Writing", "slug": "writing", "current": 6.0, "target": 7.0},
        {"name": "Speaking", "slug": "speaking", "current": 5.5, "target": 7.5},
    ])

    overall = _with_pct([
        {"name": "Overall", "slug": "overall", "current": 6.5, "target": 7.5}
    ])[0]

    practice_options = [
        {
            "name": "Listening",
            "slug": "listening",
            "desc": "40 questions. Note answers as you go, then log your score.",
        },
        {
            "name": "Reading",
            "slug": "reading",
            "desc": "60-minute timer across 3 passages. Log how many you got right.",
        },
        {
            "name": "Writing",
            "slug": "writing",
            "desc": "Task 1, Task 2, or a full 60-minute test.",
        },
        {
            "name": "Speaking",
            "slug": "speaking",
            "desc": "Log the band you were assessed at.",
        },
        {
            "name": "LRW",
            "slug": "lrw",
            "desc": "Combined Listening, Reading and Writing mock.",
            "combined": True,
        },
        {
            "name": "LR",
            "slug": "lr",
            "desc": "Combined Listening and Reading mock.",
            "combined": True,
        },
    ]

    context = {
        "user_name": "Roshan",
        "exam_date": "19 Oct 2026",
        "days_to_exam": days_to_exam(),
        "overall": overall,
        "modules": modules,
        "practice_options": practice_options,
    }
    return render(request, "core/home.html", context)
