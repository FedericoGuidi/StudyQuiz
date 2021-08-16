from django.urls import path
from studyquiz import views

urlpatterns = [
    path("", views.HomeListView.as_view(), name="home"),
    path("login/", views.login, name="login"),
    path('exam/', views.exam, name='exam'),
    path('send_exam/', views.send_exam, name='send_exam'),
    path("import/", views.import_questions, name="import"),
    path("contact/", views.contact, name="contact"),
    path("results/", views.results, name="results")
]
