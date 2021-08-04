from django.urls import path
from studyquiz import views

urlpatterns = [
    path("", views.home, name="home")
]
