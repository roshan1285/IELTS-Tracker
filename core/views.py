from django.shortcuts import render
from datetime import date

from django.contrib.auth import login
from .forms import SignUpForm

# Create your views here.

MAX_BAND = 9.0

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()

    return render(request, "core/signup.html", {"form": form})

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

    theme_preference = 0

    modules = _with_pct([
        {"name": "Listening", "slug": "listening", "current": 8.0, "target": 8.0},
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
        'theme_preference': theme_preference,
    }
    return render(request, "core/home.html", context)


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import WritingTest
from .forms import WritingSetupForm, WritingScoreForm

DURATION_MINUTES = {"task1": 20, "task2": 40, "full": 60}


# @login_required
def writing_setup(request):
    """Pick Task 1 / Task 2 / Full, optionally paste prompt(s) and upload
    the Task 1 visual, then start the timed sheet."""
    if request.method == "POST":
        form = WritingSetupForm(request.POST, request.FILES)
        if form.is_valid():
            test = form.save(commit=False)
            test.user = request.user
            test.save()
            return redirect("writing_practice", pk=test.pk)
    else:
        form = WritingSetupForm()

    return render(request, "core/writing/setup.html", {"form": form})


# @login_required
def writing_practice(request, pk):
    """The timed split-screen sheet. Both task textareas stay in the DOM
    the whole time (just hidden/shown) so switching tabs on a Full test
    never loses text — nothing is submitted until Finish is pressed."""
    test = get_object_or_404(WritingTest, pk=pk, user=request.user)

    if request.method == "POST":
        test.task1_answer = request.POST.get("task1_answer", "")
        test.task2_answer = request.POST.get("task2_answer", "")
        test.status = "completed"
        test.completed_at = timezone.now()
        test.save()
        return redirect("writing_score", pk=test.pk)

    context = {
        "test": test,
        "duration_seconds": DURATION_MINUTES[test.task_type] * 60,
    }
    return render(request, "core/writing/practice.html", context)


# @login_required
def writing_score(request, pk):
    """After finishing (or ending early), enter the assessed band(s)."""
    test = get_object_or_404(WritingTest, pk=pk, user=request.user)

    if request.method == "POST":
        form = WritingScoreForm(request.POST)
        if form.is_valid():
            test.task1_score = form.cleaned_data.get("task1_score")
            test.task2_score = form.cleaned_data.get("task2_score")
            test.save()
            return redirect("home")
    else:
        form = WritingScoreForm()

    return render(request, "core/writing/score.html", {"form": form, "test": test})