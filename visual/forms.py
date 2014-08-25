from django import forms
from django.utils import timezone
from visual.models import Session

class SessionForm(forms.ModelForm):

    session_datetime = forms.DateTimeField(initial = timezone.now,
            widget=forms.DateTimeInput(attrs={'style': 'display:none;'}))
    query = forms.CharField(max_length=1000, help_text="Enter your query")

    class Meta:
        model = Session
