from django.shortcuts import render
from datetime import date

from django.contrib.auth import login
from .forms import SignUpForm

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .utils import calculate_listening_band_score, calculate_reading_band_score, round_to_half

from .models import ListeningTest, ReadingTest, WritingTest, SpeakingTest
from .forms import WritingSetupForm, WritingScoreForm, RawScoreForm, SpeakingScoreForm, ProfileSettingsForm

import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST

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

    return render(request, "core/sign_up.html", {"form": form})

def days_to_exam(target_date):
    today = date.today()

    # target_date = date(2026, 10, 19)

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


@login_required
def home(request):
    # --- Static placeholder data. Replace with real queries once the
    # models exist, e.g. TestRecord.objects.filter(user=request.user)... ---

    theme_preference = 0
    last_no_tests=5
    last_listening_tests=ListeningTest.objects.filter(user=request.user).order_by("taken_at").only("score")[:last_no_tests]
    last_reading_tests=ReadingTest.objects.filter(user=request.user).order_by("taken_at").only("score")[:last_no_tests]
    last_writing_tests=WritingTest.objects.filter(user=request.user, status="completed").order_by("completed_at").only("task1_score", "task2_score")[:last_no_tests]
    last_speaking_tests=SpeakingTest.objects.filter(user=request.user).order_by("taken_at").only("score")[:last_no_tests]

    if last_listening_tests.count() != 0:
        try:
            listening_scores = [0.0 if t.score is None else t.score for t in last_listening_tests]
            no_listening_tests=len(listening_scores)
            listening_score= round_to_half(sum(listening_scores)/no_listening_tests)
            listening_band=calculate_listening_band_score(listening_score)
        except:
            listening_band=0.0
    else:
        listening_band=0.0

    if last_reading_tests.count() != 0:
        try:
            reading_scores = [0.0 if t.score is None else t.score for t in last_reading_tests]
            no_reading_tests=len(reading_scores)
            reading_score= round_to_half(sum(reading_scores)/no_reading_tests)
            reading_band=calculate_reading_band_score(reading_score)
        except:
            reading_band=0.0
    else:
        reading_band=0.0

    if last_writing_tests.count() != 0:
        try:
            writing_scores = [0.0 if t.overall_score is None else float(str(t.overall_score)) for t in last_writing_tests]
            no_writing_tests=len(writing_scores)
            writing_band= round_to_half(sum(writing_scores)/no_writing_tests)
        except:
            writing_band=0.0
    else:
        writing_band=0.0

    if last_speaking_tests.count() != 0:
        try:
            speaking_scores = [0.0 if t.score is None else float(str(t.score)) for t in last_speaking_tests]
            no_speaking_tests=len(speaking_scores)
            speaking_band= round_to_half(sum(speaking_scores)/no_speaking_tests)
        except:
            speaking_band=0.0
    else: 
        speaking_band=0.0
  

    targeted_listening=float(str(request.user.TL)) or 0.0
    targeted_reading=float(str(request.user.TR)) or 0.0
    targeted_writing=float(str(request.user.TW)) or 0.0
    targeted_speaking=float(str(request.user.TS)) or 0.0

    overall_band = round_to_half(
        (listening_band + reading_band + writing_band + speaking_band) / 4
    )
    targeted_overall_band=float(str(request.user.TO))

    modules = _with_pct([
        {"name": "Listening", "slug": "listening", "current": listening_band, "target": targeted_listening},
        {"name": "Reading", "slug": "reading", "current": reading_band, "target": targeted_reading},
        {"name": "Writing", "slug": "writing", "current": writing_band, "target": targeted_writing},
        {"name": "Speaking", "slug": "speaking", "current": speaking_band, "target": targeted_speaking},
    ])

    overall = _with_pct([
        {"name": "Overall", "slug": "overall", "current": overall_band, "target": targeted_overall_band}
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
            "name": "LR",
            "slug": "lr",
            "desc": "Combined Listening and Reading mock.",
            "combined": True,
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
       
    ]
    # print("Days to exam: ",days_to_exam(request.user.exam_date))
    context = {
       
        "overall": overall,
        "modules": modules,
        "practice_options": practice_options,
        'theme_preference': theme_preference,
    }
    return render(request, "core/home.html", context)



DURATION_MINUTES = {"task1": 20, "task2": 40, "full": 60}


@login_required
def writing_setup(request):
    """Pick Task 1 / Task 2 / Full, optionally paste prompt(s) and upload
    the Task 1 visual, then start the timed sheet."""
    if request.method == "POST":
        form = WritingSetupForm(request.POST, request.FILES)
        if form.is_valid():
            test = form.save(commit=False)
            test.user = request.user
            test.save()
            return redirect("core:writing_practice", pk=test.pk)
    else:
        form = WritingSetupForm()

    return render(request, "core/writing/setup.html", {"form": form})


@login_required
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
        return redirect("core:writing_score", pk=test.pk)

    context = {
        "test": test,
        "duration_seconds": DURATION_MINUTES[test.task_type] * 60,
    }
    return render(request, "core/writing/practice.html", context)


@login_required
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

@login_required
def writing_tests(request):
    tests_objs = WritingTest.objects.filter(user=request.user).order_by('started_at').only('task_type', 'status', 'task1_score', 'task2_score', 'completed_at', 'started_at')
    context={'tests':tests_objs
    }
    return render(request, "core/writing/tests.html", context)

QUESTION_RANGE = range(1, 41)


def _collect_answers(request):
    return [request.POST.get(f"q{i}", "") for i in QUESTION_RANGE]


@login_required
def listening_practice(request):
    if request.method == "POST":
        test = ListeningTest.objects.create(
            user=request.user,
            answers=_collect_answers(request),
        )
        # CHECK FOR REMARK MODE SCORE
        calculated_score = request.POST.get('calculated_score')
        if calculated_score and calculated_score.isdigit():
            test.score = int(calculated_score)
            test.save() # Your model automatically applies the band score here
            return redirect("home") # Skip manual entry!
        return redirect("core:listening_score", pk=test.pk)

    return render(request, "core/listening_practice.html", {"question_range": QUESTION_RANGE})


@login_required
def listening_score(request, pk):
    test = get_object_or_404(ListeningTest, pk=pk, user=request.user)
    if request.method == "POST":
        form = RawScoreForm(request.POST)
        if form.is_valid():
            test.score = form.cleaned_data["score"]
            test.save()
            return redirect("home")
    else:
        form = RawScoreForm()

    return render(request, "core/score_entry.html", {"form": form, "label": "Listening"})

@login_required
def listening_tests(request):
    tests = ListeningTest.objects.filter(user=request.user)

    if tests.count() != 0:
        last_tests = tests[:5]
        last_tests_count = last_tests.count()
        average_scores = [ i.score for i in last_tests ]
        average_bands = [ i.band for i in last_tests ]

        average_score= round(sum(average_scores)/last_tests_count)
        average_band = round(sum(average_bands)/last_tests_count)

    else:
            average_band=0
            average_score=0

    context={
        "test_type": "Listening",
        "tests": tests,
        "average_score": average_score,
        "average_band": float(average_band),
    }
    return render(request, "core/listening_reading_tests.html", context)

@login_required
def reading_practice(request):
    if request.method == "POST":
        test = ReadingTest.objects.create(
            user=request.user,
            answers=_collect_answers(request),
        )
        # CHECK FOR REMARK MODE SCORE
        calculated_score = request.POST.get('calculated_score')
        if calculated_score and calculated_score.isdigit():
            test.score = int(calculated_score)
            test.save() # Your model automatically applies the band score here
            return redirect("home") # Skip manual entry!
        return redirect("core:reading_score", pk=test.pk)

    return render(request, "core/reading_practice.html", {"question_range": QUESTION_RANGE})


@login_required
def reading_score(request, pk):
    test = get_object_or_404(ReadingTest, pk=pk, user=request.user)
    if request.method == "POST":
        form = RawScoreForm(request.POST)
        if form.is_valid():
            test.score = form.cleaned_data["score"]
            test.save()
            return redirect("home")
    else:
        form = RawScoreForm()

    return render(request, "core/score_entry.html", {"form": form, "label": "Reading"})

@login_required
def reading_revisit(request, pk):
    test = get_object_or_404(ReadingTest, pk=pk, user=request.user)

    form  = RawScoreForm(instance=test)
    return render(request, "core/reading_practice.html", {"form": form, "lebel": "Reading"})

@login_required
def reading_tests(request):
    tests = ReadingTest.objects.filter(user=request.user)
    print(tests.count() )
    if tests.count() > 0:
        last_tests = tests[:5]
        last_tests_count = last_tests.count()
        average_scores = [ i.score for i in last_tests ]
        average_bands = [ i.band for i in last_tests ]
        print(average_scores)
        average_score= round(sum(average_scores)/last_tests_count)
        average_band = round(sum(average_bands)/last_tests_count)
    else:
        average_band=0
        average_score=0

    context={
        "test_type": "Reading",
        "tests": tests,
        "average_score": average_score,
        "average_band": float(average_band),
    }
    return render(request, "core/listening_reading_tests.html", context)

@login_required
def speaking_practice(request):
    if request.method == "POST":
        form = SpeakingScoreForm(request.POST)
        if form.is_valid():
            SpeakingTest.objects.create(user=request.user, score=form.cleaned_data["score"])
            return redirect("home")
    else:
        form=SpeakingScoreForm()
            
    return render(request, "core/speaking_practice.html", {"form": form})


@login_required
def speaking_tests(request):
    tests_objs = SpeakingTest.objects.filter(user=request.user).order_by('taken_at').only('taken_at', 'score')
    context={'tests':tests_objs
    }
    return render(request, "core/speaking_tests.html", context)

@login_required
def settings_view(request):
    if request.method == "POST":
        form=ProfileSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = ProfileSettingsForm(instance=request.user)

    return render(request,"core/settings.html", {"form":form})

@login_required
@require_POST
def toggle_theme(request):
    data = json.loads(request.body)
    new_theme = data.get("theme")
    
    # Check against your integer choices: 0 (Light) or 1 (Dark)
    if new_theme in [0, 1]:
        request.user.preferred_theme = new_theme
        request.user.save(update_fields=["preferred_theme"])
        return JsonResponse({"status": "success", "theme": new_theme})
        
    return JsonResponse({"status": "error"}, status=400)

def ielts_band_calculator(request):

    return render(request,"core/calculator.html")