from django import forms

from testform.models import Session


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ('name',)
