from django.urls import path

from testform.views.session import SessionCreateView, SessionView, SessionsView
from testform.views.signup import PupilCreateView
from testform.views.teacher import TeachersView, TeacherView

urlpatterns = [
    path('sign-up/', PupilCreateView.as_view(), name='sign-up'),

    path('teachers/', TeachersView.as_view(), name='teachers'),
    path('teachers/<pk>/', TeacherView.as_view(), name='teacher'),
    path('teachers/<pk>/session/', SessionCreateView.as_view(), name='teacher-session'),

    path('sessions/', SessionsView.as_view(), name='sessions'),
    path('sessions/<pk>/', SessionView.as_view(), name='session'),
]