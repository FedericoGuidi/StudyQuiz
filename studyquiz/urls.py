from django.urls import path
from studyquiz import views
from studyquiz.models import Esame

urlpatterns = [
    path("", views.HomeListView.as_view(), name="home"),
    path("hello/<slug:name>", views.hello_there, name="hello"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
]
