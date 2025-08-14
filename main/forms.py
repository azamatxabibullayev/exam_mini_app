from django import forms
from .models import Choice


class TakeTestForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super().__init__(*args, **kwargs)
        for question in questions:
            self.fields[f"question_{question.id}"] = forms.ModelChoiceField(
                queryset=question.choices.all(),
                widget=forms.RadioSelect,
                required=True,
                label=question.text
            )
