from django import forms
from django.utils import timezone
from models import Search


class SearchForm(forms.ModelForm):

    datetime = forms.DateTimeField(initial=timezone.now,
                                   widget=forms.DateTimeInput(
                                       attrs={'style': 'display:none;'}))
    text = forms.CharField(max_length=200)

    class Meta:
        model = Search
