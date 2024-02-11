from django import forms

from testform.models import Review


class SessionForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('name', 'star', 'end', 'state')
