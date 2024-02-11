from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import FormView, DetailView, ListView

from testform.forms.session import SessionForm
from testform.models import Session


class SessionsView(ListView):
    model = Session
    template_name = 'sessions.html'
    queryset = Session.objects.all()


class SessionView(DetailView):
    model = Session
    template_name = 'session.html'


class SessionCreateView(FormView):
    template_name = 'session-create.html'
    form_class = SessionForm

    def get_success_url(self):
        context = self.get_context_data()
        return reverse_lazy('teacher', kwargs={'pk': context['teacher'].id})

    def get_context_data(self, **kwargs):
        context = super(SessionCreateView, self).get_context_data(**kwargs)
        context['teacher'] = User.objects.get(id=self.kwargs.get('pk'))

        return context

    def form_valid(self, form):
        if form.is_valid():
            context = self.get_context_data()
            session: Session = form.save(commit=False)
            session.teacher_id = context['teacher'].id
            session.save()

        return super(SessionCreateView, self).form_valid(form)
