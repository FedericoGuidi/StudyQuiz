from io import TextIOWrapper
from django.http.response import HttpResponseRedirect
from studyquiz.forms import DomandaForm, UploadCSVForm
from django.shortcuts import redirect, render
from django.views import generic
from django.forms import modelformset_factory
from bson import ObjectId

from datetime import datetime

from studyquiz.models import Domanda, Esame, Results, Test, FileCSV


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


def import_questions(request):
    esami = Esame.objects.all()
    if request.method == 'POST':
        exam_id = request.POST['exam']
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            f = TextIOWrapper(request.FILES['file'].file, encoding='UTF-8-sig', errors='replace')
            questions_num = FileCSV.handle_CSV(exam_id, f)
            status = 'OK'
            return render(request, "studyquiz/import.html", { 'exam_list': esami, 'status': status, 'questions_num': questions_num })
    else:
        form = UploadCSVForm()
    return render(request, 'studyquiz/import.html', {'form': form, 'exam_list': esami })


def contact(request):
    return render(request, "studyquiz/contact.html")


def exam(request):
    exam_id = request.POST['exam']
    test = Test.retrieve(exam_id, 5)
    DomandaFormSet = modelformset_factory(Domanda, form=DomandaForm, extra=0)
    formset = DomandaFormSet(queryset=test.domande)
    return render(request, "studyquiz/exam.html", {'formset': formset, "exam": test.esame})


def send_exam(request):
    exam_id = request.POST['exam']
    DomandaFormSet = modelformset_factory(Domanda, form=DomandaForm, extra=0)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        formset = DomandaFormSet(request.POST)
        # check whether it's valid:
        if formset.is_valid():
            # process the data in form.cleaned_data as required
            risposte = [data['risposta_id'] for data in formset.cleaned_data]
            domande = [data['_id'] for data in formset.cleaned_data]
            request.session['grade'] = Test.grade(risposte)
            request.session['total'] = len(domande)
            # redirect to a new URL:
            return redirect('/results/')
        else:
            exam = Esame.objects.get(pk=ObjectId(exam_id))

    # if a GET (or any other method) we'll create a blank form
    else:
        formset = DomandaFormSet()

    return render(request, 'studyquiz/exam.html', {'formset': formset, 'exam': exam})


def results(request):
    grade = request.session.get('grade')
    total = request.session.get('total')
    percent = (grade * 100) / total
    results = Results(grade, total, percent)
    return render(request, "studyquiz/results.html", {'results': results})


def login(request):
    return render(request, "studyquiz/login.html")
