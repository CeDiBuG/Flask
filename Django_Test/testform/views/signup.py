from django.contrib.auth.models import User, Group
from django.urls import reverse_lazy
from django.views.generic import FormView
from testform.forms.pupil import PupilForm


class PupilCreateView(FormView):
    template_name = 'sign-up.html'
    form_class = PupilForm
    success_url = reverse_lazy('sessions')

    def form_valid(self, form):
        if form.is_valid():
            pupil: User = form.save()
            pupil_group = Group.objects.get(name='pupil')
            pupil_group.user_set.add(pupil)

        return super(PupilCreateView, self).form_valid(form)
