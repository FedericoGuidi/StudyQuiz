from django.shortcuts import render, redirect
from django.views.generic import ListView

from datetime import datetime

from studyquiz.forms import EsameForm
from studyquiz.models import Esame, Test

class HomeListView(ListView):
    """Renders the home page, with a list of all exams."""
    model = Esame
    context_object_name = "exam_list"
    template_name = "studyquiz/home.html"

    def get_queryset(self):
        
        return Esame.retrieve_exams()

class TestListView(ListView):
    model = Test
    context_object_name = "domande_list"
    template_name = "studyquiz/exam.html"

    def get_queryset(self, id):
        return Test.retrieve_test(id)

def home(request):
    return render(request, "studyquiz/home.html")

def about(request):
    return render(request, "studyquiz/about.html")

def contact(request):
    return render(request, "studyquiz/contact.html")

def start_exam(request):
    exam_id = request.POST['exam']
    test = Test.retrieve_test(exam_id)
    return render(request, "studyquiz/exam.html", {"domande_list": test.domande })