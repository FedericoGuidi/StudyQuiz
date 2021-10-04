from django.urls import path
from studyquiz import views

urlpatterns = [
    path("", views.HomeListView.as_view(), name="home"),
    path('exam/', views.exam, name='exam'),
    path('send_exam/', views.send_exam, name='send_exam'),
    path("import/", views.import_questions, name="import"),
    path("contact/", views.contact, name="contact"),
    path("results/", views.results, name="results"),
    path("logout/", views.logout, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("check_answer/", views.check_answer, name="check_answer")
]
