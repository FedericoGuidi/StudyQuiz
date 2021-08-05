from django.shortcuts import render, redirect
from django.views.generic import ListView

from datetime import datetime

from studyquiz.forms import EsameForm
from studyquiz.models import Esame

class HomeListView(ListView):
    """Renders the home page, with a list of all exams."""
    model = Esame
    context_object_name = "exam_list"
    template_name = "studyquiz/home.html"

    def get_queryset(self):
        return Esame.retrieve_exams()


def home(request):
    return render(request, "studyquiz/home.html")

def about(request):
    return render(request, "studyquiz/about.html")

def contact(request):
    return render(request, "studyquiz/contact.html")

def hello_there(request, name):
    return render(
        request,
        'studyquiz/hello_there.html',
        {
            'name': name,
            'date': datetime.now()
        }
    )

def inizia_esame(request):
    form = EsameForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.log_date = datetime.now()
            message.save()
            return redirect("home")
    else:
        return render(request, "studyquiz/esame.html", {"form": form})