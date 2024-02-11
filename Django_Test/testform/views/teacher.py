from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView


class TeachersView(TemplateView):
    template_name = 'teachers.html'

    def get(self, request, *args, **kwargs):

        teachers = User.objects.all()
        context = {'teachers': teachers}

        return render(request, self.template_name, context)


class TeacherView(DetailView):
    model = User
    template_name = 'teacher.html'
