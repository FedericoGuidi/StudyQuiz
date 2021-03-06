from io import TextIOWrapper
import random

from django.http.response import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from studyquiz.forms import DomandaForm, UploadCSVForm
from django.shortcuts import redirect, render
from django.views import generic
from django.forms import modelformset_factory
from bson import ObjectId

from studyquiz.models import Domanda, Esame, Results, Test, FileCSV, Utenti

from django.contrib.auth import get_user, logout as log_out
from django.conf import settings
from django.http import HttpResponseRedirect
from urllib.parse import urlencode


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


def questions(request):
    return render(request, "studyquiz/questions.html")


def dashboard(request):
    user = get_user(request)
    user_info = Utenti.retrieve(user.id)
    return render(request, "studyquiz/dashboard.html", { 'user_info': user_info })


def exam(request):
    exam_id = request.POST['exam']
    multiple_questions_num = request.POST['multiple_questions_num']
    open_questions_num = request.POST['open_questions_num']
    from_lesson = request.POST['from_lesson']
    to_lesson = request.POST['to_lesson']
    practice_mode = 'practice_mode' in request.POST

    if multiple_questions_num in (None, ''):
        multiple_questions_num = 23
    else:
        multiple_questions_num = int(multiple_questions_num)

    if open_questions_num in (None, ''):
        open_questions_num = 2
    else:
        open_questions_num = int(open_questions_num)

    if from_lesson in (None, ''):
        from_lesson = 0
    else:
        from_lesson = int(from_lesson)

    if to_lesson in (None, ''):
        to_lesson = 999
    else:
        to_lesson = int(to_lesson)

    test = Test.retrieve(exam_id, multiple_questions_num, open_questions_num, from_lesson, to_lesson)
    DomandaFormSet = modelformset_factory(Domanda, form=DomandaForm, extra=0)
    formset = DomandaFormSet(queryset=test.domande)
    view = "studyquiz/practice.html" if practice_mode else "studyquiz/exam.html"
    return render(request, view, {'formset': formset, "exam": test.esame, "domande_aperte": test.domande_aperte})


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
            domande = [str(data['_id'].pk) for data in formset.cleaned_data]
            request.session['grade'] = Test.grade(domande, risposte)
            request.session['total'] = len(domande)
            request.session['domande'] = domande
            request.session['risposte'] = risposte
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
    domande = request.session.get('domande')
    risposte = request.session.get('risposte')
    domande_id = []
    risposte_id = []
    for d in domande:
        domande_id.append(ObjectId(d))
    for r in risposte:
        risposte_id.append(ObjectId(r))
    results = Results(grade, total, domande_id, risposte_id)
    return render(request, "studyquiz/results.html", {'results': results})


def check_answer(request):
    question = request.GET['question']
    answer = request.GET['answer']
    ordered_answers = request.GET.getlist('ordered_answers[]')
    risposte = Domanda.retrieve_questions(question)
    risposte = [risposta for a in ordered_answers for risposta in risposte if risposta.pk == ObjectId(a)]
    correct_answer = next((r for r in risposte if r.corretta), None)
    data = {}
    data['html'] = render_to_string(request=request, template_name="studyquiz/_correct_answer.html", context={'risposte': risposte, 'selected_answer': ObjectId(answer) })
    data['point'] = 1 if correct_answer.pk == ObjectId(answer) else 0
    return JsonResponse(data)


def logout(request):
    log_out(request)
    return_to = urlencode({'returnTo': request.build_absolute_uri('/')})
    logout_url = 'https://%s/v2/logout?client_id=%s&%s' % \
                 (settings.SOCIAL_AUTH_AUTH0_DOMAIN, settings.SOCIAL_AUTH_AUTH0_KEY, return_to)
    return HttpResponseRedirect(logout_url)
