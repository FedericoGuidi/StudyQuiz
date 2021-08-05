from django.urls import path
from studyquiz import views
from studyquiz.models import Esame

urlpatterns = [
    path("", views.HomeListView.as_view(), name="home"),
    path("exam/", views.TestListView.as_view(), name="exam"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path('start_exam/', views.start_exam, name='start_exam')
]
