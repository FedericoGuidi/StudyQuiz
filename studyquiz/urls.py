from django.urls import path
from studyquiz import views
from studyquiz.models import Esame

urlpatterns = [
    path("", views.HomeListView.as_view(), name="home"),
    path("login/", views.login, name="login"),
    path('exam/', views.exam, name='exam'),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
]
