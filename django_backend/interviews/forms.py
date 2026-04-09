from django import forms
from .models import Interview


class InterviewStartForm(forms.Form):
    role = forms.CharField(max_length=100, required=True)
    interview_type = forms.ChoiceField(
        choices=Interview.INTERVIEW_TYPES,
        initial='mixed'
    )
    total_questions = forms.IntegerField(min_value=3, max_value=20, initial=5)
