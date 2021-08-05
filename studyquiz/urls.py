from django.urls import path
from studyquiz import views

urlpatterns = [
    path("", views.home, name="home"),
    path("hello/<slug:name>", views.hello_there, name="hello"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
]
