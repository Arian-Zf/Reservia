from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.services, name="services"),
    path("book/", views.book, name="book"),
    path("my/", views.my_appointments, name="my_appointments"),
    path("my/<int:pk>/cancel/", views.cancel_appointment, name="cancel_appointment"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("register/", views.register, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
