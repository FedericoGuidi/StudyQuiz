from django.shortcuts import render
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.views import generic

from datetime import datetime

from studyquiz.models import Esame, Test


class HomeListView(generic.ListView):
    """Renders the home page, with a list of all exams."""
    model = Esame
    context_object_name = "exam_list"
    template_name = "studyquiz/home.html"

    def get_queryset(self):
        return Esame.objects.all()


class TestListView(generic.ListView):
    model = Test
    context_object_name = "domande_list"
    template_name = "studyquiz/exam.html"


def home(request):
    return render(request, "studyquiz/home.html")


def about(request):
    return render(request, "studyquiz/about.html")


def contact(request):
    return render(request, "studyquiz/contact.html")


def exam(request):
    exam_id = request.POST['exam']
    test = Test.retrieve(exam_id)
    return render(request, "studyquiz/exam.html", {"domande_list": test.domande, "exam": test.esame})


def login(request):
    return render(request, "studyquiz/login.html")
