from django import forms
from .models import WritingTest

from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class SignUpForm(UserCreationForm):
    full_name = forms.CharField(max_length=150, label="Full name")

    TL = forms.DecimalField(
        label="Targeted Listening",
        widget=forms.NumberInput(attrs={'step': '0.5', 'min': '0', 'max': '9'})
    )
    TR = forms.DecimalField(
        label="Targeted Reading",
        widget=forms.NumberInput(attrs={'step': '0.5', 'min': '0', 'max': '9'})
    )
    TW = forms.DecimalField(
        label="Targeted Writing",
        widget=forms.NumberInput(attrs={'step': '0.5', 'min': '0', 'max': '9'})
    )
    TS = forms.DecimalField(
        label="Targeted Speaking",
        widget=forms.NumberInput(attrs={'step': '0.5', 'min': '0', 'max': '9'})
    )
    TO = forms.DecimalField(
        label="Targeted Overall",
        widget=forms.NumberInput(attrs={'step': '0.5', 'min': '0', 'max': '9'})
    )

    exam_date = forms.DateField(
        label="Exam Date (booked/targeted)",
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = CustomUser
        fields = ("username", "full_name", "TL", "TR", "TW", "TS", "TO", "exam_date")


class WritingSetupForm(forms.ModelForm):
    class Meta:
        model = WritingTest
        fields = ["task_type", "task1_prompt", "task1_image", "task2_prompt"]
        widgets = {
            "task_type": forms.RadioSelect,
            "task1_prompt": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Paste the Task 1 prompt text (optional)",
                "spellcheck": "false",
            }),
            "task2_prompt": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Paste the Task 2 prompt text (optional)",
                "spellcheck": "false",
            }),
        }


class WritingScoreForm(forms.Form):
    task1_score = forms.DecimalField(
        max_digits=3, decimal_places=1, min_value=0, max_value=9,
        required=False,
        widget=forms.NumberInput(attrs={"step": "0.5", "placeholder": "e.g. 6.5"}),
    )
    task2_score = forms.DecimalField(
        max_digits=3, decimal_places=1, min_value=0, max_value=9,
        required=False,
        widget=forms.NumberInput(attrs={"step": "0.5","placeholder": "e.g. 6.5"}),
    )
    
class RawScoreForm(forms.Form):
    score = forms.IntegerField(
        min_value=0, max_value=40,
        widget=forms.NumberInput(attrs={"placeholder": "out of 40"}),
    )
