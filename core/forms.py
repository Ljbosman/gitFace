from django import forms
from .models import MergeRequest

class MergeRequestCreationForm(forms.ModelForm):

    class Meta:
        model = MergeRequest
        fields = ('title', 'repo', 'source_branch', 'target_branch', 'target_email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['repo'].widget = forms.Select(choices=[])
        self.fields['source_branch'].widget = forms.Select(choices=[])
        self.fields['target_branch'].widget = forms.Select(choices=[])
